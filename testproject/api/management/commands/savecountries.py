import requests

from django.core.management.base import BaseCommand, CommandError


from api.models import Country


class Command(BaseCommand):
    help = "Saves country to the database"

    def handle(self, *args, **options):
        API = "https://www.eib.org"
        self.stdout.write(self.style.SUCCESS(
            "Fetching data from {}".format(API)))

        endpoint = "/provider-eib-plr/app/loans/list/filters?language=EN&propertyNames=countries"
        response = requests.get(API + endpoint)

        if response.status_code != 200:
            raise CommandError("API returned an error")

        data = response.json()
        if "filters" not in data:
            raise CommandError("API returned an error")

        filters = data["filters"]
        if "countries" not in filters:
            raise CommandError("API returned an invalid data")

        countries = filters.get("countries", [])
        saved_country = 0
        self.stdout.write(self.style.SUCCESS("Saving countries"))

        for country in countries:
            value = country.get("value", "")
            label = country.get("label", "")

            Country.objects.get_or_create(value=value, label=label)
            saved_country += 1

        self.stdout.write(self.style.SUCCESS(
            "Successfully saved {} countries".format(saved_country)))
