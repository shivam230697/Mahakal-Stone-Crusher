from django import forms
from .models import Party, WeighbridgeEntry, ProductionEntry, Expense, Payment, MiningEntry, SalesInvoice
class DateInput(forms.DateInput):
    input_type = "date"
class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ["name","party_type","phone","address","gstin","opening_balance","opening_balance_type"]
        widgets = {"address": forms.Textarea(attrs={"rows":2})}
class WeighbridgeForm(forms.ModelForm):
    class Meta:
        model = WeighbridgeEntry
        fields = ["date","slip_no","entry_type","vehicle_no","driver_name","party","product","gross_weight","tare_weight","measured_quantity","quantity_unit","rate","remarks"]
        widgets = {"date": forms.DateTimeInput(attrs={"type":"datetime-local"})}
class ProductionForm(forms.ModelForm):
    class Meta:
        model = ProductionEntry
        fields = ["date","product","quantity","quantity_unit","raw_material_used","raw_material_unit","wastage","shift","remarks"]
        widgets = {"date": DateInput()}
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["date","category","description","amount","paid_to","payment_mode"]
        widgets = {"date": DateInput()}
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["date","party","payment_type","amount","mode","reference","notes"]
        widgets = {"date": DateInput()}


class MiningForm(forms.ModelForm):
    class Meta:
        model = MiningEntry
        fields = ["date","entry_no","vehicle_no","driver_name","measurement_method",
                  "gross_weight","tare_weight","trip_count","average_trip_quantity","quantity_unit",
                  "excavator_hours","dumper_hours","diesel_litres","remarks"]
        widgets = {"date": forms.DateTimeInput(attrs={"type":"datetime-local"})}


class SalesInvoiceForm(forms.ModelForm):
    class Meta:
        model = SalesInvoice
        fields = ["invoice_no","date","customer","product","quantity","quantity_unit","rate","gst_percent","notes"]
        widgets = {"date": DateInput(), "notes": forms.Textarea(attrs={"rows": 2})}
