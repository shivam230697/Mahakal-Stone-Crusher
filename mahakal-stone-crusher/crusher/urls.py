from django.urls import path
from . import views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("weighbridge/", views.weighbridge_list, name="weighbridge"),
    path("weighbridge/add/", views.weighbridge_add, name="weighbridge_add"),
    path("production/", views.production_list, name="production"),
    path("production/add/", views.production_add, name="production_add"),
    path("parties/", views.party_list, name="parties"),
    path("parties/add/", views.party_add, name="party_add"),
    path("expenses/", views.expense_list, name="expenses"),
    path("expenses/add/", views.expense_add, name="expense_add"),
    path("payments/", views.payment_list, name="payments"),
    path("payments/add/", views.payment_add, name="payment_add"),
    path("stock/", views.stock_report, name="stock"),
    path("invoices/", views.invoice_list, name="invoices"),
    path("invoices/add/", views.invoice_add, name="invoice_add"),
    path("mining/", views.mining_list, name="mining"),
    path("mining/add/", views.mining_add, name="mining_add"),
]
