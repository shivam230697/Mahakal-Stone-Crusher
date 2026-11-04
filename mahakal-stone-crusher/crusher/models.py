from django.db import models
from django.utils import timezone
from decimal import Decimal

PRODUCTS = ["10mm", "20mm", "40mm", "Dust", "Gitti", "M-Sand", "Boulder"]

class Party(models.Model):
    PARTY_TYPES = [("CUSTOMER", "Customer"), ("SUPPLIER", "Supplier"), ("BOTH", "Both")]
    name = models.CharField(max_length=160)
    party_type = models.CharField(max_length=12, choices=PARTY_TYPES, default="CUSTOMER")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    opening_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    opening_balance_type = models.CharField(max_length=8, choices=[("DR","Receivable"),("CR","Payable")], default="DR")
    gstin = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Product(models.Model):
    name = models.CharField(max_length=40, unique=True)
    unit = models.CharField(max_length=8, default="MT")
    active = models.BooleanField(default=True)
    def __str__(self): return self.name

class WeighbridgeEntry(models.Model):
    TYPES = [("INWARD","Inward"),("OUTWARD","Outward")]
    date = models.DateTimeField(default=timezone.now)
    slip_no = models.CharField(max_length=40, unique=True)
    entry_type = models.CharField(max_length=10, choices=TYPES)
    vehicle_no = models.CharField(max_length=20)
    driver_name = models.CharField(max_length=100, blank=True)
    party = models.ForeignKey(Party, on_delete=models.PROTECT, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    gross_weight = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    tare_weight = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    net_weight = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    measured_quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    quantity_unit = models.CharField(max_length=8, choices=[("MT", "Tonnes (MT)"), ("CFT", "Cubic feet (CFT)")], default="MT")
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remarks = models.TextField(blank=True)
    def save(self, *args, **kwargs):
        self.net_weight = max(Decimal("0"), self.gross_weight - self.tare_weight)
        if self.entry_type == "OUTWARD" and self.measured_quantity == 0 and self.quantity_unit == "MT":
            self.measured_quantity = self.net_weight
        super().save(*args, **kwargs)
    @property
    def amount(self): return self.net_weight * self.rate
    def __str__(self): return self.slip_no

class ProductionEntry(models.Model):
    date = models.DateField(default=timezone.localdate)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    quantity_unit = models.CharField(max_length=8, choices=[("MT", "Tonnes (MT)"), ("CFT", "Cubic feet (CFT)")], default="MT")
    raw_material_used = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    raw_material_unit = models.CharField(max_length=8, choices=[("MT", "Tonnes (MT)"), ("CFT", "Cubic feet (CFT)")], default="MT")
    wastage = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    shift = models.CharField(max_length=20, blank=True)
    remarks = models.TextField(blank=True)
    def __str__(self): return f"{self.date} - {self.product}"

class Expense(models.Model):
    date = models.DateField(default=timezone.localdate)
    category = models.CharField(max_length=80)
    description = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    paid_to = models.CharField(max_length=120, blank=True)
    payment_mode = models.CharField(max_length=20, default="Cash")
    def __str__(self): return f"{self.category} - {self.amount}"

class Payment(models.Model):
    TYPES = [("RECEIVED","Received"),("PAID","Paid")]
    date = models.DateField(default=timezone.localdate)
    party = models.ForeignKey(Party, on_delete=models.PROTECT)
    payment_type = models.CharField(max_length=10, choices=TYPES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    mode = models.CharField(max_length=20, default="Cash")
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    def __str__(self): return f"{self.party} {self.payment_type} {self.amount}"


class MiningEntry(models.Model):
    MEASUREMENT_CHOICES = [("WEIGHBRIDGE", "Weighbridge"), ("TRIPS", "Trip-based")]
    date = models.DateTimeField(default=timezone.now)
    entry_no = models.CharField(max_length=40, unique=True)
    vehicle_no = models.CharField(max_length=20)
    driver_name = models.CharField(max_length=100, blank=True)
    measurement_method = models.CharField(max_length=12, choices=MEASUREMENT_CHOICES)
    gross_weight = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    tare_weight = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    trip_count = models.PositiveIntegerField(default=0)
    average_trip_quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    quantity_unit = models.CharField(max_length=8, choices=[("MT", "Tonnes (MT)"), ("CFT", "Cubic feet (CFT)")], default="MT")
    excavator_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    dumper_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    diesel_litres = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.measurement_method == "WEIGHBRIDGE":
            self.quantity = max(Decimal("0"), self.gross_weight - self.tare_weight)
            self.quantity_unit = "MT"
        else:
            self.quantity = Decimal(self.trip_count) * self.average_trip_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.entry_no} - {self.vehicle_no}"


class SalesInvoice(models.Model):
    invoice_no = models.CharField(max_length=40, unique=True)
    date = models.DateField(default=timezone.localdate)
    customer = models.ForeignKey(Party, on_delete=models.PROTECT, limit_choices_to={"party_type__in": ["CUSTOMER", "BOTH"]})
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    quantity_unit = models.CharField(max_length=8, choices=[("MT", "Tonnes (MT)"), ("CFT", "Cubic feet (CFT)")], default="MT")
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    @property
    def taxable_amount(self):
        return self.quantity * self.rate

    @property
    def gst_amount(self):
        return self.taxable_amount * self.gst_percent / Decimal("100")

    @property
    def grand_total(self):
        return self.taxable_amount + self.gst_amount

    def __str__(self):
        return self.invoice_no
