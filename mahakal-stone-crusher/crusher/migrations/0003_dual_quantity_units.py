from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("crusher", "0002_miningentry")]
    operations = [
        migrations.AddField(
            model_name="miningentry", name="quantity_unit",
            field=models.CharField(choices=[("MT","Tonnes (MT)"),("CFT","Cubic feet (CFT)")], default="MT", max_length=8),
        ),
        migrations.AddField(
            model_name="productionentry", name="quantity_unit",
            field=models.CharField(choices=[("MT","Tonnes (MT)"),("CFT","Cubic feet (CFT)")], default="MT", max_length=8),
        ),
        migrations.AddField(
            model_name="productionentry", name="raw_material_unit",
            field=models.CharField(choices=[("MT","Tonnes (MT)"),("CFT","Cubic feet (CFT)")], default="MT", max_length=8),
        ),
    ]
