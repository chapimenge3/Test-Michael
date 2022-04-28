import requests

from django.core.management.base import BaseCommand
from django.utils import timezone

from api.models import Projects, Country, Sector, Loans


class Command(BaseCommand):
    help = "Saves project to the database"

    def add_arguments(self, parser):
        parser.add_argument('--filter', default=None, type=str)

    def construct_filter(self):
        filters = {
            "sortColumn": "loanParts.loanPartStatus.statusDate",
            "sortDir": "desc",
            "pageNumber": 0,
            "itemPerPage": 100,
            "pageable": True,
            "language": "EN",
            "defaultLanguage": "EN",
            "loanPartYearFrom": 1959,
            "loanPartYearTo": timezone.now().year,
            "orCountries.region": True,
            "orCountries": True,
            "orSectors": True,
        }
        return filters

    def handle(self, *args, **options):
        API = "https://www.eib.org"

        if options.get("filter", None):
            filters = options.get("filter")
            filters = {i.split("=")[0]: i.split("=")[1]
                       for i in filters.split("&")}
        else:
            filters = self.construct_filter()

        saved = 0
        endpoint = "/provider-eib-plr/app/loans/list"
        for i in range(10):
            self.stdout.write(self.style.SUCCESS(
                "Running for Page {}".format(i)))

            filters['pageNumber'] = i
            response = requests.get(API + endpoint, params=filters)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(
                    "Error request returned {}".format(response.status_code)))
                continue

            if "data" not in response.json():
                self.stdout.write(self.style.ERROR(
                    "Error while fetching data"))
                continue

            data = response.json()['data']
            for loan in data:
                title = loan.get("title", "")
                if loan.get('primaryTags', None) and isinstance(loan.get('primaryTags'), list):
                    primaryTags = loan.get('primaryTags')
                    country = Country.objects.get_or_create(
                        value=primaryTags[0]['value'], label=primaryTags[0]['label'])
                    sector = Sector.objects.get_or_create(
                        value=primaryTags[2]['value'], label=primaryTags[2]['label'])
                    project = Projects.objects.get_or_create(
                        title=title, country=country[0], sector=sector[0])
                    amount = loan['additionalInformation'][0]
                    date = loan['additionalInformation'][2]
                    Loans.objects.get_or_create(
                        project=project[0], amount=amount, date=date)

                    saved += 1

        self.stdout.write(self.style.SUCCESS(
            "Successfully saved {} Loans".format(saved)))
