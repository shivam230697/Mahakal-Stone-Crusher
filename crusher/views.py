from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import Party, Product, WeighbridgeEntry, ProductionEntry, Expense, Payment, MiningEntry, SalesInvoice
from .forms import PartyForm, WeighbridgeForm, ProductionForm, ExpenseForm, PaymentForm, MiningForm, SalesInvoiceForm
from datetime import date

@login_required
def dashboard(request):
    today = timezone.localdate()
    sales = WeighbridgeEntry.objects.filter(entry_type="OUTWARD", date__date=today)
    inward = WeighbridgeEntry.objects.filter(entry_type="INWARD", date__date=today)
    production = ProductionEntry.objects.filter(date=today)
    expenses = Expense.objects.filter(date=today)
    ctx = {
        "today": today, "sales_qty": sales.aggregate(v=Sum("net_weight"))["v"] or 0,
        "inward_qty": inward.aggregate(v=Sum("net_weight"))["v"] or 0,
        "production_qty": production.aggregate(v=Sum("quantity"))["v"] or 0,
        "sales_count": sales.count(), "expense_total": expenses.aggregate(v=Sum("amount"))["v"] or 0,
        "recent_entries": WeighbridgeEntry.objects.select_related("party","product")[:8],
        "party_count": Party.objects.count(),
    }
    return render(request, "crusher/dashboard.html", ctx)

@login_required
def generic_list(request, model, template, title):
    return render(request, template, {"rows": model.objects.all().order_by("-id")[:250], "page_title": title})

@login_required
def weighbridge_list(request):
    return generic_list(request, WeighbridgeEntry, "crusher/weighbridge.html", "Weighbridge Register")
@login_required
def production_list(request):
    return generic_list(request, ProductionEntry, "crusher/production.html", "Production Register")
@login_required
def party_list(request):
    return generic_list(request, Party, "crusher/parties.html", "Parties")
@login_required
def expense_list(request):
    return generic_list(request, Expense, "crusher/expenses.html", "Expenses")
@login_required
def payment_list(request):
    return generic_list(request, Payment, "crusher/payments.html", "Payments")

def save_form(request, form_class, template, title, success_url):
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{title} saved successfully.")
        return redirect(success_url)
    return render(request, "crusher/form.html", {"form": form, "page_title": title})

@login_required
def weighbridge_add(request): return save_form(request, WeighbridgeForm, "crusher/form.html", "Add Weighbridge Entry", "weighbridge")
@login_required
def production_add(request): return save_form(request, ProductionForm, "crusher/form.html", "Add Production Entry", "production")
@login_required
def party_add(request): return save_form(request, PartyForm, "crusher/form.html", "Add Party", "parties")
@login_required
def expense_add(request): return save_form(request, ExpenseForm, "crusher/form.html", "Add Expense", "expenses")
@login_required
def payment_add(request): return save_form(request, PaymentForm, "crusher/form.html", "Add Payment", "payments")

@login_required
def mining_list(request):
    return generic_list(request, MiningEntry, "crusher/mining.html", "Mining Register")

@login_required
def mining_add(request):
    return save_form(request, MiningForm, "crusher/form.html", "Add Mining Entry", "mining")

@login_required
def stock_report(request):
    products = Product.objects.filter(active=True)
    data = []
    for p in products:
        # Keep MT and CFT separate. Never add unlike units without a verified conversion factor.
        for unit in ["MT", "CFT"]:
            mining = MiningEntry.objects.filter(quantity_unit=unit).aggregate(v=Sum("quantity"))["v"] or 0
            if p.name != "Boulder":
                mining = 0
            inward = WeighbridgeEntry.objects.filter(product=p, entry_type="INWARD").aggregate(v=Sum("net_weight"))["v"] or 0
            produced = ProductionEntry.objects.filter(product=p, quantity_unit=unit).aggregate(v=Sum("quantity"))["v"] or 0
            outward = WeighbridgeEntry.objects.filter(product=p, entry_type="OUTWARD", quantity_unit=unit).aggregate(v=Sum("measured_quantity"))["v"] or 0
            raw_used = ProductionEntry.objects.filter(raw_material_unit=unit).aggregate(v=Sum("raw_material_used"))["v"] or 0 if p.name == "Boulder" else 0
            if unit == "MT":
                opening_inward = inward
            else:
                opening_inward = 0
            dispatch = outward
            balance = mining + opening_inward + produced - dispatch - raw_used
            if any([mining, opening_inward, produced, dispatch, raw_used]):
                data.append({"product":p, "unit":unit, "mining":mining, "inward":opening_inward,
                             "produced":produced, "outward":dispatch, "raw_used":raw_used, "balance":balance})
    return render(request, "crusher/stock.html", {"data":data, "page_title":"Product Stock"})


@login_required
def invoice_list(request):
    rows = SalesInvoice.objects.select_related("customer", "product").order_by("-date", "-id")[:250]
    return render(request, "crusher/invoices.html", {"rows": rows, "page_title": "Sales Invoices"})

@login_required
def invoice_add(request):
    return save_form(request, SalesInvoiceForm, "crusher/form.html", "Create Sales Invoice", "invoices")
