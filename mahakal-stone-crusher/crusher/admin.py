from django.contrib import admin
from .models import Party, Product, WeighbridgeEntry, ProductionEntry, Expense, Payment, MiningEntry, SalesInvoice
admin.site.register([Party, Product, WeighbridgeEntry, ProductionEntry, Expense, Payment, MiningEntry, SalesInvoice])
