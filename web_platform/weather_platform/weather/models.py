from django.db import models

class Weather(models.Model):
    datetime = models.DateTimeField()
    temp = models.FloatField()
    feelslike = models.FloatField()
    dew = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    windspeed = models.FloatField()
    windgust = models.FloatField()
    winddir = models.FloatField()
    visibility = models.FloatField()
    cloudcover = models.FloatField()
    precip = models.FloatField()
    precipprob = models.FloatField()
    uvindex = models.IntegerField()
    severerisk = models.IntegerField()
    conditions = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"Weather data for {self.datetime}"
