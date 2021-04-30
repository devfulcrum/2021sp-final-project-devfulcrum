from django.db import models


class VaccineData(models.Model):
    country = models.CharField(max_length=75)
    date = models.DateField()
    doses_administered = models.IntegerField()

    class Meta:
        db_table = 'vaccine_data'

    def __str__(self):
        # this is to make the model testable
        return "Vaccine Data for: " + self.country + " Published Date: " + self.date.__str__() + \
               " Doses Administered: " + self.doses_administered.__str__()


class CovidData(models.Model):
    country = models.CharField(max_length=75)
    date = models.DateField()
    confirmed = models.IntegerField()

    class Meta:
        db_table = 'covid_data'

    def __str__(self):
        # this is to make the model testable
        return "Covid Data for: " + self.country + " Published Date: " + self.date.__str__() + \
               " Confirmed Cases: " + self.confirmed.__str__()
