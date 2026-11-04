# Mahakal Stone Crusher ERP — starter release

A Django + Bootstrap 5 application configured for Render and PostgreSQL.

## Included in this first working release
- Login-protected dashboard
- Own mining register with weighbridge-based and trip-based quantity calculation, equipment hours and diesel litres
- Product master seeded with 10mm, 20mm, 40mm, Dust, Gitti, M-Sand, Boulder
- Weighbridge inward/outward register; net weight auto-calculated as gross minus tare
- Daily production register by product
- Party master (customer/supplier/both)
- Expense register
- Payment received/paid register
- Product stock summary with MT/CFT kept separate
- Sales invoices with customer, product, quantity in MT or CFT, rate and GST percentage
- Outward dispatch quantity can be recorded in MT or CFT (gross/tare weighbridge weights remain in MT)
- Django admin for data administration

## Run locally (Windows)
1. Install Python 3.12.
2. Open this folder in VS Code and run:
   `py -m venv venv`
   `venv\Scripts\activate`
   `pip install -r requirements.txt`
   `python manage.py migrate`
   `python manage.py seed_products`
   `python manage.py createsuperuser`
   `python manage.py runserver`
3. Open http://127.0.0.1:8000 and log in.

## Deploy on Render
1. Push the complete folder to a new GitHub repository.
2. In Render, choose **New + → Blueprint** and select the repository.
3. Render reads `render.yaml` and provisions the web service and PostgreSQL database.
4. After deploy, create the first admin user from the Render Shell:
   `python manage.py createsuperuser`
5. Log in at `/accounts/login/`.

## Important before using real accounts
This is a first functional foundation, not a finished audited accounting system. It currently does not include GST invoice posting, editable/deletable transaction audit trail, weighbridge ticket printing, purchase/sales invoices, bank reconciliation, user roles, or automatic party ledger posting. Do not enter live financial records until these controls and your exact plant workflow have been verified. Back up the database regularly and set a strong SECRET_KEY.

## Next implementation stage
- Invoice and tax/GST configuration
- Party ledger with automatic debit/credit postings
- Stock adjustment and opening stock
- Vehicle ticket print layout
- Diesel issue/consumption and machinery-wise fuel reports
- Crusher production inputs, shift, machine downtime and wastage
- Date-filtered reports and Excel/PDF export
- Permissions for admin, manager, weighbridge operator and accountant


## Mining quantity logic
- Weighbridge method: quantity = gross weight - tare weight.
- Trip method: quantity = number of trips × average quantity per trip.
- Mining extraction is included as Boulder inward stock.
- Production raw-material-used quantity is deducted from Boulder stock.
- Record each physical load only once, using either weighbridge or trip method.


## Dual quantity units (MT and CFT)
- Mining trip entries can be recorded in either tonnes (MT) or cubic feet (CFT).
- Mining weighbridge entries always calculate tonnes from gross minus tare.
- Production output and raw-material consumption each store their own unit.
- Stock reports keep MT and CFT balances separate to prevent invalid addition.
- Finished-goods dispatch quantity can be entered in MT or CFT; gross/tare weighbridge weights remain in MT. For CFT dispatches, enter the measured quantity and select CFT.
- A product-specific conversion factor must be confirmed before converting CFT to MT; no density assumption is hardcoded.
