from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.conf import settings

from games.models import CheckoutList
import requests
import pandas as pd
import os


class Command(BaseCommand):
    help = "Load checkout data into the database"

    def handle(self, *args, **kwargs):
        df = pd.read_csv(os.path.join(settings.BASE_DIR, 'database/checkoutlist.csv'))
        
        # check to see if data already exists in the database

        if not(CheckoutList.objects.all().exists()):
            checkouts = [
                CheckoutList(
                    score=row['score'],
                    dart_one=row['dart_one'],
                    dart_two=row['dart_two'],
                    dart_three=row['dart_three']
                )
                for index, row in df.iterrows()
            ]

            CheckoutList.objects.bulk_create(checkouts)
            print(f"{len(checkouts)} records inserted successfully.")
        print('Checkout data already exists')