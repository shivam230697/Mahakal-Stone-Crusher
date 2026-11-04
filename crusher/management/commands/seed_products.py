from django.core.management.base import BaseCommand
from crusher.models import Product
class Command(BaseCommand):
    help = "Create Mahakal Stone Crusher product master"
    def handle(self, *args, **kwargs):
        for name in ["10mm","20mm","40mm","Dust","Gitti","M-Sand","Boulder"]:
            Product.objects.get_or_create(name=name, defaults={"unit":"MT"})
        self.stdout.write(self.style.SUCCESS("Mahakal products created."))
