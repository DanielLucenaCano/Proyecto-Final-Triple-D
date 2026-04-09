from decimal import Decimal

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OptionalServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('static_ip', models.BooleanField(default=False)),
                ('backup_enabled', models.BooleanField(default=False)),
                ('firewall_enabled', models.BooleanField(default=False)),
                ('control_panel_enabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('STOPPED', 'Stopped'), ('RUNNING', 'Running')], default='STOPPED', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServerConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_cores', models.PositiveIntegerField(default=1)),
                ('ram_gb', models.PositiveIntegerField(default=1)),
                ('storage_type', models.CharField(choices=[('SSD', 'SSD'), ('HDD', 'HDD')], default='SSD', max_length=10)),
                ('storage_gb', models.PositiveIntegerField(default=20)),
                ('bandwidth_mbps', models.PositiveIntegerField(default=100)),
                ('os_type', models.CharField(choices=[('LINUX', 'Linux'), ('WINDOWS', 'Windows Server')], default='LINUX', max_length=20)),
                ('monthly_price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('optional_services', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='configuration', to='servers.optionalservices')),
                ('server', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='configuration', to='servers.server')),
            ],
        ),
    ]
