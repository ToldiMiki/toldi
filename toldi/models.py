from django.db import models
from django.utils import timezone

class LogMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"
    

class CNjoke(models.Model):
    id = models.BigAutoField(primary_key=True)
    errorMsg = models.CharField(max_length=1000, blank=True)
    theJoke = models.CharField(max_length=1000, blank=True)
    jokeEN = models.CharField(max_length=1000, blank=True)
    jokeHU = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        """Returns a string representation of a Joke."""
        if self.errorMsg : return f"Error:'{self.errorMsg}'"
        elif self.theJoke : return f"theJoke:'{self.theJoke}'"
        elif self.jokeEN or self.jokeHU : return f"ENG:'{self.jokeEN}' HUN:'{self.jokeHU}'"
        else: return "unnown error"
    

"""COUNTRY_CHOICES = (
    ('Magyarország','HU'),
    ('Anglia', 'GB'),
    ('Lengyelország','PL'),
    ('Spanyolország','SP'),
)


class Country(models.Model):
    theCountry = models.CharField( choices=COUNTRY_CHOICES )"""