from rest_framework import test

from django.urls import reverse
from django.test import TestCase

from api.models import Projects, Country, Sector, Loans


class APITestCase(test.APITestCase):

    def test_project(self):
        url = reverse("testapi-projects")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(isinstance(response.data, list))

    def test_countries(self):
        url = reverse("testapi-countries")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(isinstance(response.data, list))
        self.assertTrue(isinstance(response.data[0], dict))

    def test_sectors(self):
        url = reverse("testapi-sectors")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(isinstance(response.data, list))
        self.assertTrue(isinstance(response.data[0], dict))

    def test_loans(self):
        url = reverse("testapi-loans")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(isinstance(response.data, list))
        self.assertTrue(isinstance(response.data[0], dict))


class ModelTestCase(TestCase):

    def test_sector(self):
        sector = Sector.objects.create(value="value", label="label")
        self.assertTrue(isinstance(sector, Sector))
        self.assertEqual(sector.value, "value")
        self.assertEqual(sector.label, "label")

    def test_country(self):
        country = Country.objects.create(value="value", label="label")
        self.assertTrue(isinstance(country, Country))
        self.assertEqual(country.value, "value")
        self.assertEqual(country.label, "label")

    def test_project(self):
        sector = Sector.objects.create(value="value", label="label")
        country = Country.objects.create(value="value", label="label")
        project = Projects.objects.create(
            sector=sector,
            country=country,
            title="title")

        self.assertTrue(isinstance(project, Projects))
        self.assertEqual(project.title, "title")
        self.assertEqual(project.sector, sector)
        self.assertEqual(project.country, country)
    
    def test_loan(self):
        sector = Sector.objects.create(value="value", label="label")
        country = Country.objects.create(value="value", label="label")
        project = Projects.objects.create(
            sector=sector,
            country=country,
            title="title")
        loans = Loans.objects.create(
            project=project,
            amount="$100",
            date="1 April 2020",
        )
        
        self.assertTrue(isinstance(loans, Loans))
        self.assertEqual(loans.project, project)
        self.assertEqual(loans.amount, "$100")
        self.assertEqual(loans.date, "1 April 2020")

