#!/usr/bin/env bash
# Install deps
pip install -r requirements.txt

# Run migrations automatically
python manage.py migrate
