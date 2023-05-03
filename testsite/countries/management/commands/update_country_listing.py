import json
import os

import requests
from countries.models import Country, Region
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads country data from a JSON file."
    IMPORT_FILE = os.path.join(settings.BASE_DIR, "..", "data", "countries.json")

    def get_data(self):
        print('Downloading input data from remote...')
        resp = requests.get('https://storage.googleapis.com/dcr-django-test/countries.json')
        if resp.status_code == 200:
            data = resp.json()
        else:
            print('WARNING: Could not download input data from URL. Fallback to default file.')
            with open(self.IMPORT_FILE) as f:
                data = json.load(f)
        return data

    def handle(self, *args, **options):
        data = self.get_data()
        for row in data:
            region, region_created = Region.objects.get_or_create(name=row["region"])
            if region_created:
                self.stdout.write(
                    self.style.SUCCESS("Region: {} - Created".format(region))
                )
            country, country_created = Country.objects.get_or_create(
                name=row["name"],
                defaults={
                    "alpha2Code": row["alpha2Code"],
                    "alpha3Code": row["alpha3Code"],
                    "population": row["population"],
                    "region": region,
                    'capital': row['capital'],
                    'top_level_domain': row['topLevelDomain'][0]
                },
            )

            if not country_created:
                country.top_level_domain = row['topLevelDomain'][0]
                country.capital = row['capital']
                country.save()

            self.stdout.write(
                self.style.SUCCESS(
                    "{} - {}".format(
                        country, "Created" if country_created else "Updated"
                    )
                )
            )
