from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PricingBreakdown:
    base_price: Decimal
    windows_license: Decimal
    static_ip: Decimal
    backup: Decimal
    firewall: Decimal
    control_panel: Decimal
    total_price: Decimal


class PricingService:
    VCPU_PRICE = Decimal('4.0')
    RAM_PRICE = Decimal('2.5')
    SSD_PRICE = Decimal('0.08')
    HDD_PRICE = Decimal('0.025')
    BANDWIDTH_BLOCK_PRICE = Decimal('2.0')
    WINDOWS_LICENSE_PRICE = Decimal('15.0')
    STATIC_IP_PRICE = Decimal('3.0')
    FIREWALL_PRICE = Decimal('2.0')
    CONTROL_PANEL_PRICE = Decimal('12.0')
    BACKUP_PERCENTAGE = Decimal('0.20')

    @classmethod
    def calculate_monthly_price(
        cls,
        *,
        cpu_cores: int,
        ram_gb: int,
        storage_type: str,
        storage_gb: int,
        bandwidth_mbps: int,
        os_type: str,
        static_ip: bool,
        backup_enabled: bool,
        firewall_enabled: bool,
        control_panel_enabled: bool,
    ) -> PricingBreakdown:
        storage_unit_price = cls.SSD_PRICE if storage_type == 'SSD' else cls.HDD_PRICE
        bandwidth_blocks = Decimal(str(bandwidth_mbps)) / Decimal('100')

        base_price = (
            Decimal(cpu_cores) * cls.VCPU_PRICE
            + Decimal(ram_gb) * cls.RAM_PRICE
            + Decimal(storage_gb) * storage_unit_price
            + bandwidth_blocks * cls.BANDWIDTH_BLOCK_PRICE
        )

        windows_license = cls.WINDOWS_LICENSE_PRICE if os_type == 'WINDOWS' else Decimal('0.0')
        static_ip_price = cls.STATIC_IP_PRICE if static_ip else Decimal('0.0')
        backup_price = (base_price * cls.BACKUP_PERCENTAGE) if backup_enabled else Decimal('0.0')
        firewall_price = cls.FIREWALL_PRICE if firewall_enabled else Decimal('0.0')
        control_panel_price = cls.CONTROL_PANEL_PRICE if control_panel_enabled else Decimal('0.0')

        total_price = (
            base_price
            + windows_license
            + static_ip_price
            + backup_price
            + firewall_price
            + control_panel_price
        )

        return PricingBreakdown(
            base_price=base_price,
            windows_license=windows_license,
            static_ip=static_ip_price,
            backup=backup_price,
            firewall=firewall_price,
            control_panel=control_panel_price,
            total_price=total_price,
        )
