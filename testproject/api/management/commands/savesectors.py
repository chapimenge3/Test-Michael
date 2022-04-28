import requests

from django.core.management.base import BaseCommand, CommandError


from api.models import Sector


class Command(BaseCommand):
    help = "Saves sectors to the database"

    def handle(self, *args, **options):
        API = "https://www.eib.org"
        endpoint = "/provider-eib-plr/app/loans/list/filters?language=EN&propertyNames=sectors"

        self.stdout.write(self.style.SUCCESS(
            "Fetching sectors from {}".format(API)))

        response = requests.get(API + endpoint)
        if response.status_code != 200:
            raise CommandError("API returned an error")

        data = response.json()
        if "filters" not in data:
            raise CommandError("API returned an error")

        filters = data["filters"]
        if "sectors" not in filters:
            raise CommandError("API returned an invalid data")

        sectors = filters.get("sectors", [])

        self.stdout.write(self.style.SUCCESS("Saving Sectors"))
        saved_sectors = 0
        for sector in sectors:
            value = sector.get("value", "")
            label = sector.get("label", "")
            Sector.objects.get_or_create(value=value, label=label)
            saved_sectors += 1
        self.stdout.write(self.style.SUCCESS(
            "Successfully saved {} sectors".format(saved_sectors)))
