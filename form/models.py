from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Form(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.name} form"

    def get_absolute_url(self):
        return reverse("view_form", kwargs={'id': self.id})

    

class FormSection(models.Model):
    name = models.CharField(max_length=500)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} section"

class InputField(models.Model):
    label = models.TextField()
    section = models.ForeignKey(FormSection, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.label} question"

class InputTextField(models.Model):
    label = models.TextField()
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.label} question"

class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    assessment = models.OneToOneField("assessment.assessment", on_delete=models.CASCADE)
    fields = models.JSONField()

    def __str__(self):
        return f"response to form {self.form_id}"
    
    def get_absolute_url(self):
        return reverse("response", kwargs={'id': self.id})

class TextFieldResponse(models.Model):
    answer = models.TextField()
    question = models.ForeignKey(InputTextField, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.label} question"