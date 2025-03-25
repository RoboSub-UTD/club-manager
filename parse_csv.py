import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clubManager.settings')
from clubManager import settings

import django
django.setup()

import csv
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import make_aware
from payments.models import Payment, Product, Term
from django.contrib.auth.models import User
from events.models import UserIdentification

def parse_csv_and_store_data(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                comet_card_id = row['comet_card_id'].strip()
                net_id = row["net_id"].strip().lower()
                # first_name = row['First Name'].strip()
                # last_name = row['Last Name'].strip()
                name = row["name"].strip()
                first_name, last_name = name.split(' ', 1)

                # Create or get the user
                user, created = User.objects.get_or_create(
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'username': net_id,
                    },
                    username=net_id
                )
                
                UserIdentification.objects.update_or_create(
                    defaults={
                        'user': user,
                        'student_id': comet_card_id
                    },
                    user=user,
                    student_id=comet_card_id
                )
            except Exception as e:
                print(f"Error processing row: {row}")
                print(e)

# Call the function with the path to your CSV file
parse_csv_and_store_data('users.csv')
