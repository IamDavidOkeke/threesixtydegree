from django.db import models
from django.urls import reverse
from .helpers import email_body_template, email_subject_template
from django.core.mail import send_mail
import os
import uuid
from survey.models import Survey
from record.models import Record

# Create your models here.

class Assessment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    evaluator_name = models.CharField(max_length=500)
    evaluator_email = models.EmailField()
    evaluator_relationship = models.CharField(max_length=500)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('view_evaluator', kwargs = {
            'id': self.id
        })
    

    def generate_body(self, request):
        mail_template = self.survey.email_template
        if mail_template == '':
            mail_template = email_body_template
        a = mail_template.replace('[Name of person giving Feedback]', self.evaluator_name).replace('[Name of person being assessed]', f'{self.record.first_name} {self.record.last_name}').replace('[Link to provide feedback]', request.build_absolute_uri(reverse('respond', kwargs={'id': self.survey.form.id, 'ev_id':self.id}))).replace('[Name of administrator]', f'{request.user.first_name} {request.user.last_name}')

        return a
    
    def send_assessment_mail(self, request):
        subject = email_subject_template
        body = self.generate_body(request)
        sender = os.getenv('EMAIL_HOST_USER')

        return send_mail(subject, body, sender, [self.evaluator_email], fail_silently=False)