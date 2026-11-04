from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [("crusher", "0003_dual_quantity_units")]
    operations = [
        migrations.AddField(
            model_name="weighbridgeentry",
            name="measured_quantity",
            field=models.DecimalField(decimal_places=3, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="weighbridgeentry",
            name="quantity_unit",
            field=models.CharField(choices=[("MT", "Tonnes (MT)"), ("CFT", "Cubic feet (CFT)")], default="MT", max_length=8),
        ),
        migrations.CreateModel(
            name="SalesInvoice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("invoice_no", models.CharField(max_length=40, unique=True)),
                ("date", models.DateField(default=django.utils.timezone.localdate)),
                ("quantity", models.DecimalField(decimal_places=3, max_digits=12)),
                ("quantity_unit", models.CharField(choices=[("MT", "Tonnes (MT)"), ("CFT", "Cubic feet (CFT)")], default="MT", max_length=8)),
                ("rate", models.DecimalField(decimal_places=2, max_digits=12)),
                ("gst_percent", models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ("notes", models.TextField(blank=True)),
                ("customer", models.ForeignKey(limit_choices_to={"party_type__in": ["CUSTOMER", "BOTH"]}, on_delete=django.db.models.deletion.PROTECT, to="crusher.party")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="crusher.product")),
            ],
        ),
    ]
