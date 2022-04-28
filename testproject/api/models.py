from django.db import models


class BaseModel(models.Model):
    value = models.CharField(max_length=255)
    label = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.label


class Country(BaseModel):
    pass


class Sector(BaseModel):
    pass


class Projects(models.Model):
    title = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Loans(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    amount = models.CharField(max_length=255) # TODO make this decimal value
    date = models.CharField(max_length=255) # TODO make this datetime field

    def __str__(self):
        return self.project.title
