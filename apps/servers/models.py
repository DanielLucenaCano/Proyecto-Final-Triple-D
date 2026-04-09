from decimal import Decimal

from django.conf import settings
from django.db import models


class ServerStatus(models.TextChoices):
    STOPPED = 'STOPPED', 'Stopped'
    RUNNING = 'RUNNING', 'Running'


class StorageType(models.TextChoices):
    SSD = 'SSD', 'SSD'
    HDD = 'HDD', 'HDD'


class OSType(models.TextChoices):
    LINUX = 'LINUX', 'Linux'
    WINDOWS = 'WINDOWS', 'Windows Server'


class Server(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='servers')
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=ServerStatus.choices, default=ServerStatus.STOPPED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name} ({self.user.username})'


class OptionalServices(models.Model):
    static_ip = models.BooleanField(default=False)
    backup_enabled = models.BooleanField(default=False)
    firewall_enabled = models.BooleanField(default=False)
    control_panel_enabled = models.BooleanField(default=False)


class ServerConfiguration(models.Model):
    server = models.OneToOneField(Server, on_delete=models.CASCADE, related_name='configuration')
    cpu_cores = models.PositiveIntegerField(default=1)
    ram_gb = models.PositiveIntegerField(default=1)
    storage_type = models.CharField(max_length=10, choices=StorageType.choices, default=StorageType.SSD)
    storage_gb = models.PositiveIntegerField(default=20)
    bandwidth_mbps = models.PositiveIntegerField(default=100)
    os_type = models.CharField(max_length=20, choices=OSType.choices, default=OSType.LINUX)
    optional_services = models.OneToOneField(OptionalServices, on_delete=models.CASCADE, related_name='configuration')
    monthly_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Config: {self.server.name}'
