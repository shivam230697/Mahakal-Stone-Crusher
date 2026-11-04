from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Party", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=160)), ("party_type", models.CharField(choices=[("CUSTOMER","Customer"),("SUPPLIER","Supplier"),("BOTH","Both")], default="CUSTOMER", max_length=12)),
            ("phone", models.CharField(blank=True,max_length=20)), ("address", models.TextField(blank=True)),
            ("opening_balance", models.DecimalField(decimal_places=2,default=0,max_digits=14)),
            ("opening_balance_type", models.CharField(choices=[("DR","Receivable"),("CR","Payable")],default="DR",max_length=8)),
            ("gstin", models.CharField(blank=True,max_length=20)), ("created_at",models.DateTimeField(auto_now_add=True))]),
        migrations.CreateModel(name="Product", fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
            ("name",models.CharField(max_length=40,unique=True)),("unit",models.CharField(default="MT",max_length=8)),("active",models.BooleanField(default=True))]),
        migrations.CreateModel(name="WeighbridgeEntry", fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
            ("date",models.DateTimeField(default=django.utils.timezone.now)),("slip_no",models.CharField(max_length=40,unique=True)),
            ("entry_type",models.CharField(choices=[("INWARD","Inward"),("OUTWARD","Outward")],max_length=10)),
            ("vehicle_no",models.CharField(max_length=20)),("driver_name",models.CharField(blank=True,max_length=100)),
            ("gross_weight",models.DecimalField(decimal_places=3,default=0,max_digits=12)),("tare_weight",models.DecimalField(decimal_places=3,default=0,max_digits=12)),
            ("net_weight",models.DecimalField(decimal_places=3,default=0,max_digits=12)),("rate",models.DecimalField(decimal_places=2,default=0,max_digits=12)),
            ("remarks",models.TextField(blank=True)),("party",models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.PROTECT,to="crusher.party")),
            ("product",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to="crusher.product"))]),
        migrations.CreateModel(name="ProductionEntry", fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("date",models.DateField(default=django.utils.timezone.localdate)),
            ("quantity",models.DecimalField(decimal_places=3,max_digits=12)),("raw_material_used",models.DecimalField(decimal_places=3,default=0,max_digits=12)),
            ("wastage",models.DecimalField(decimal_places=3,default=0,max_digits=12)),("shift",models.CharField(blank=True,max_length=20)),("remarks",models.TextField(blank=True)),
            ("product",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to="crusher.product"))]),
        migrations.CreateModel(name="Expense", fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("date",models.DateField(default=django.utils.timezone.localdate)),
            ("category",models.CharField(max_length=80)),("description",models.CharField(blank=True,max_length=200)),("amount",models.DecimalField(decimal_places=2,max_digits=14)),
            ("paid_to",models.CharField(blank=True,max_length=120)),("payment_mode",models.CharField(default="Cash",max_length=20))]),
        migrations.CreateModel(name="Payment", fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("date",models.DateField(default=django.utils.timezone.localdate)),
            ("payment_type",models.CharField(choices=[("RECEIVED","Received"),("PAID","Paid")],max_length=10)),("amount",models.DecimalField(decimal_places=2,max_digits=14)),
            ("mode",models.CharField(default="Cash",max_length=20)),("reference",models.CharField(blank=True,max_length=100)),("notes",models.TextField(blank=True)),
            ("party",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to="crusher.party"))])
    ]
