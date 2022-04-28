import requests

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import status

from django.utils import timezone

API = "https://www.eib.org"


class TestAPI(viewsets.ViewSet):

    def get_data(self, API, endpoint, request):
        """Fetch data from the given API

        Args:
            API (str): Base endpoint of the API
            endpoint (str): the endpoint of the API
            request (str): the request object to get the query parameters to filter the data

        Returns:
            requests.Response: return response object of requests with the return data of the API
        """

        # You can use the following filter the same with the EIB API
        year = timezone.now().year
        search = request.query_params.get('search', "")
        sortColumn = request.query_params.get(
            'sortColumn', "loanParts.loanPartStatus.statusDate")
        sortDir = request.query_params.get('sortDir', "desc")
        pageNumber = request.query_params.get('pageNumber', 0)
        itemPerPage = request.query_params.get('itemPerPage', 100)
        pageable = request.query_params.get('pageable', True)
        language = request.query_params.get('language', "EN")
        defaultLanguage = request.query_params.get('defaultLanguage', "EN")
        loanPartYearFrom = request.query_params.get('loanPartYearFrom', 2010)
        loanPartYearTo = request.query_params.get('loanPartYearTo', year)
        countries_region = request.query_params.get('countries.region', None)
        orCountries_region = request.query_params.get(
            'orCountries.region', True)
        countries = request.query_params.get('countries', None)
        orCountries = request.query_params.get('orCountries', True)
        sectors = request.query_params.get('sectors', None)
        orSectors = request.query_params.get('orSectors', True)

        # Build filter string for the API request
        filter = ""

        filter += "search=" + search
        filter += "&sortColumn=" + sortColumn
        filter += "&sortDir=" + sortDir
        filter += "&pageNumber=" + str(pageNumber)
        filter += "&itemPerPage=" + str(itemPerPage)

        # if filter contains country region
        if countries_region:
            filter += "&countries.region=" + countries_region

        # if filter contains sectors
        if sectors:
            filter += "&sectors=" + sectors

        # if filter contains countries
        if countries:
            filter += "&countries=" + countries

        filter += "&orCountries.region=" + str(orCountries_region)
        filter += "&orCountries=" + str(orCountries)
        filter += "&orSectors=" + str(orSectors)
        filter += "&pageable=" + 'true' if pageable else 'false'
        filter += "&language=" + language
        filter += "&defaultLanguage=" + defaultLanguage
        filter += "&loanPartYearFrom=" + str(loanPartYearFrom)
        filter += "&loanPartYearTo=" + str(loanPartYearTo)

        # TODO - Add filters to request params by making the filter dictionary
        response = requests.get(API + endpoint + filter)

        return response

    @action(methods=['GET'], detail=False, url_path='countries', url_name='countries')
    def countries(self, _):
        """Get a list of country available from the site

        Returns:
            list: return a list of countries
        """
        endpoint = "/provider-eib-plr/app/loans/list/filters?language=EN&propertyNames=countries"
        response = requests.get(API + endpoint)

        if response.status_code != 200:
            return Response("Something is Wrong", status=status.HTTP_400_BAD_REQUEST)

        data = response.json()
        if "filters" not in data:
            return Response("Something is Wrong", status=status.HTTP_400_BAD_REQUEST)

        filters = data["filters"]

        if "countries" not in filters:
            return Response("Something is Wrong", status=status.HTTP_400_BAD_REQUEST)

        countries_list = filters.get("countries", [])

        return Response(countries_list, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='sectors', url_name='sectors')
    def sectors(self, request):
        """Get a list of sectors from the site

        Returns:
            list: return a list of sectors
        """
        endpoint = "/provider-eib-plr/app/loans/list/filters?language=EN&propertyNames=sectors"
        response = requests.get(API + endpoint)

        if response.status_code != 200:
            return Response("Something is Wrong", status=status.HTTP_400_BAD_REQUEST)

        data = response.json()
        if "filters" not in data:
            return Response("Something is Wrong", status=status.HTTP_400_BAD_REQUEST)

        filters = data["filters"]

        if "sectors" not in filters:
            return Response("Something is Wrong", status=status.HTTP_400_BAD_REQUEST)

        sectors = filters.get("sectors", [])
        return Response(sectors, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='projects', url_name='projects')
    def project_list(self, request):
        """Get a list of project titles from the site

        Returns:
            list: return a list of project titles
        """

        endpoint = "/provider-eib-plr/app/loans/list?"

        response = self.get_data(API, endpoint, request)

        if response.status_code != 200:
            return Response("Something is Wrong", status=status.HTTP_400_BAD_REQUEST)

        if "data" not in response.json():
            return Response("Something is Wrong", status=status.HTTP_400_BAD_REQUEST)

        data = response.json()['data']

        project_titles = [project['title'] for project in data]

        return Response(project_titles, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='loans', url_name='loans')
    def loans(self, request):
        """Get list of loans from the site

        Returns:
            list: return a list of loans recieved from the site
        """

        endpoint = "/provider-eib-plr/app/loans/list?"

        response = self.get_data(API, endpoint, request)

        if response.status_code != 200:
            return Response("Something is Wrong", status=status.HTTP_400_BAD_REQUEST)

        if "data" not in response.json():
            return Response("Something is Wrong", status=status.HTTP_400_BAD_REQUEST)

        data = response.json()['data']

        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='filters', url_name='filters')
    def get_filter_params(self, _):
        """Get filter parameters for sending requests

        Returns:
            list: return a list of filter parameters
        """
        filters = ["search", "sortColumn", "sortDir", "pageNumber", "itemPerPage", "pageable", "language", "defaultLanguage",
                   "loanPartYearFrom", "loanPartYearTo", "countries_region", "orCountries_region", "countries", "orCountries", "sectors", "orSectors"]
        return Response(filters, status=status.HTTP_200_OK)
