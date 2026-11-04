from django.db import migrations, models
import django.utils.timezone
class Migration(migrations.Migration):
    dependencies = [("crusher", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="MiningEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("entry_no", models.CharField(max_length=40, unique=True)),
                ("vehicle_no", models.CharField(max_length=20)),
                ("driver_name", models.CharField(blank=True, max_length=100)),
                ("measurement_method", models.CharField(choices=[("WEIGHBRIDGE","Weighbridge"),("TRIPS","Trip-based")], max_length=12)),
                ("gross_weight", models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ("tare_weight", models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ("trip_count", models.PositiveIntegerField(default=0)),
                ("average_trip_quantity", models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ("quantity", models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ("excavator_hours", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ("dumper_hours", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ("diesel_litres", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("remarks", models.TextField(blank=True)),
            ],
        ),
    ]
