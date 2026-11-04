#!/usr/bin/env bash
set -o errexit
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_products
python manage.py collectstatic --no-input
