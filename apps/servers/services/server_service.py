import json
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.pricing.services.pricing_service import PricingService
from apps.servers.models import OptionalServices, Server, ServerConfiguration, ServerStatus


class ServerService:
    @staticmethod
    def parse_body(raw_body: bytes) -> dict[str, Any]:
        if not raw_body:
            return {}
        return json.loads(raw_body.decode('utf-8'))

    @staticmethod
    @transaction.atomic
    def create_server(user, payload: dict[str, Any]) -> Server:
        required = ['name', 'cpu_cores', 'ram_gb', 'storage_type', 'storage_gb', 'bandwidth_mbps', 'os_type']
        missing = [field for field in required if payload.get(field) in (None, '')]
        if missing:
            raise ValidationError(f'Campos requeridos faltantes: {", ".join(missing)}')

        server = Server.objects.create(user=user, name=payload['name'])
        optional_services = OptionalServices.objects.create(
            static_ip=payload.get('static_ip', False),
            backup_enabled=payload.get('backup_enabled', False),
            firewall_enabled=payload.get('firewall_enabled', False),
            control_panel_enabled=payload.get('control_panel_enabled', False),
        )

        pricing = PricingService.calculate_monthly_price(
            cpu_cores=payload['cpu_cores'],
            ram_gb=payload['ram_gb'],
            storage_type=payload['storage_type'],
            storage_gb=payload['storage_gb'],
            bandwidth_mbps=payload['bandwidth_mbps'],
            os_type=payload['os_type'],
            static_ip=optional_services.static_ip,
            backup_enabled=optional_services.backup_enabled,
            firewall_enabled=optional_services.firewall_enabled,
            control_panel_enabled=optional_services.control_panel_enabled,
        )

        ServerConfiguration.objects.create(
            server=server,
            cpu_cores=payload['cpu_cores'],
            ram_gb=payload['ram_gb'],
            storage_type=payload['storage_type'],
            storage_gb=payload['storage_gb'],
            bandwidth_mbps=payload['bandwidth_mbps'],
            os_type=payload['os_type'],
            optional_services=optional_services,
            monthly_price=pricing.total_price,
        )
        return server

    @staticmethod
    @transaction.atomic
    def update_server(server: Server, payload: dict[str, Any]) -> Server:
        server.name = payload.get('name', server.name)
        server.save(update_fields=['name', 'updated_at'])

        config = server.configuration
        optional_services = config.optional_services

        for field in ['cpu_cores', 'ram_gb', 'storage_type', 'storage_gb', 'bandwidth_mbps', 'os_type']:
            if field in payload:
                setattr(config, field, payload[field])

        for field in ['static_ip', 'backup_enabled', 'firewall_enabled', 'control_panel_enabled']:
            if field in payload:
                setattr(optional_services, field, payload[field])
        optional_services.save()

        pricing = PricingService.calculate_monthly_price(
            cpu_cores=config.cpu_cores,
            ram_gb=config.ram_gb,
            storage_type=config.storage_type,
            storage_gb=config.storage_gb,
            bandwidth_mbps=config.bandwidth_mbps,
            os_type=config.os_type,
            static_ip=optional_services.static_ip,
            backup_enabled=optional_services.backup_enabled,
            firewall_enabled=optional_services.firewall_enabled,
            control_panel_enabled=optional_services.control_panel_enabled,
        )
        config.monthly_price = pricing.total_price
        config.save()
        return server

    @staticmethod
    def start_server(server: Server) -> Server:
        server.status = ServerStatus.RUNNING
        server.save(update_fields=['status', 'updated_at'])
        return server

    @staticmethod
    def stop_server(server: Server) -> Server:
        server.status = ServerStatus.STOPPED
        server.save(update_fields=['status', 'updated_at'])
        return server

    @staticmethod
    def serialize_server(server: Server) -> dict[str, Any]:
        config = server.configuration
        optional_services = config.optional_services

        return {
            'id': server.id,
            'name': server.name,
            'status': server.status,
            'configuration': {
                'cpu_cores': config.cpu_cores,
                'ram_gb': config.ram_gb,
                'storage_type': config.storage_type,
                'storage_gb': config.storage_gb,
                'bandwidth_mbps': config.bandwidth_mbps,
                'os_type': config.os_type,
                'monthly_price': float(config.monthly_price),
                'optional_services': {
                    'static_ip': optional_services.static_ip,
                    'backup_enabled': optional_services.backup_enabled,
                    'firewall_enabled': optional_services.firewall_enabled,
                    'control_panel_enabled': optional_services.control_panel_enabled,
                },
            },
        }
