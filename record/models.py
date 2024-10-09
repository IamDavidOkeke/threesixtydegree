from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from survey.models import Survey


# Create your models here.

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    email = models.EmailField()
    role = models.CharField(max_length=500)
    survey = models.ManyToManyField(Survey)

    def get_absolute_url(self):
        return reverse('record', kwargs={'id': self.id})
