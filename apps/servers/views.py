from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.pricing.services.pricing_service import PricingService
from apps.servers.models import Server
from apps.servers.services.server_service import ServerService


@method_decorator([csrf_exempt, login_required], name='dispatch')
class ServerCollectionView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        servers = Server.objects.filter(user=request.user).select_related('configuration__optional_services')
        data = [ServerService.serialize_server(server) for server in servers]
        return JsonResponse({'results': data}, status=200)

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            payload = ServerService.parse_body(request.body)
            server = ServerService.create_server(request.user, payload)
            return JsonResponse(ServerService.serialize_server(server), status=201)
        except ValidationError as exc:
            return JsonResponse({'error': str(exc)}, status=400)


@method_decorator([csrf_exempt, login_required], name='dispatch')
class ServerDetailView(View):
    def patch(self, request: HttpRequest, server_id: int, *args, **kwargs) -> JsonResponse:
        try:
            payload = ServerService.parse_body(request.body)
            server = get_object_or_404(Server.objects.select_related('configuration__optional_services'), id=server_id, user=request.user)
            updated = ServerService.update_server(server, payload)
            return JsonResponse(ServerService.serialize_server(updated), status=200)
        except ValidationError as exc:
            return JsonResponse({'error': str(exc)}, status=400)


@method_decorator([csrf_exempt, login_required], name='dispatch')
class ServerStartView(View):
    def post(self, request: HttpRequest, server_id: int, *args, **kwargs) -> JsonResponse:
        server = get_object_or_404(Server, id=server_id, user=request.user)
        ServerService.start_server(server)
        return JsonResponse({'message': 'Servidor iniciado.', 'status': server.status}, status=200)


@method_decorator([csrf_exempt, login_required], name='dispatch')
class ServerStopView(View):
    def post(self, request: HttpRequest, server_id: int, *args, **kwargs) -> JsonResponse:
        server = get_object_or_404(Server, id=server_id, user=request.user)
        ServerService.stop_server(server)
        return JsonResponse({'message': 'Servidor detenido.', 'status': server.status}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class PriceCalculatorView(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        payload = ServerService.parse_body(request.body)
        pricing = PricingService.calculate_monthly_price(
            cpu_cores=payload.get('cpu_cores', 1),
            ram_gb=payload.get('ram_gb', 1),
            storage_type=payload.get('storage_type', 'SSD'),
            storage_gb=payload.get('storage_gb', 20),
            bandwidth_mbps=payload.get('bandwidth_mbps', 100),
            os_type=payload.get('os_type', 'LINUX'),
            static_ip=payload.get('static_ip', False),
            backup_enabled=payload.get('backup_enabled', False),
            firewall_enabled=payload.get('firewall_enabled', False),
            control_panel_enabled=payload.get('control_panel_enabled', False),
        )

        return JsonResponse(
            {
                'base_price': float(pricing.base_price),
                'windows_license': float(pricing.windows_license),
                'static_ip': float(pricing.static_ip),
                'backup': float(pricing.backup),
                'firewall': float(pricing.firewall),
                'control_panel': float(pricing.control_panel),
                'total_price': float(pricing.total_price),
            },
            status=200,
        )
