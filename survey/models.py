from form.models import Form
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Survey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    email_template = models.TextField(max_length=1000)

    def get_absolute_url(self):
        return reverse('view_survey', kwargs={'id': self.id})