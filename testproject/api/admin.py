from django.contrib import admin

from api.models import Country, Sector, Projects, Loans

admin.site.register(Country)
admin.site.register(Sector)
admin.site.register(Projects)
admin.site.register(Loans)
