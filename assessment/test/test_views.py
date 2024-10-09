from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from assessment.models import Assessment
from record.models import Record
from form.models import Form
from survey.models import Survey
from assessment.helpers import email_body_template

class AssessmentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user= User.objects.create_user(username="username", password="password", email="example@email.com")
        cls._client = Client()
        cls._client.login(username='username', password='password')
        cls.test_form = Form.objects.create(name='name', description='description', user=cls.user)
        cls.test_survey = Survey.objects.create(title='title', form=cls.test_form, email_template=email_body_template, user=cls.user)
        cls.test_record = Record.objects.create(first_name='first_name', last_name='last_name', role='role', email='example@mail.com', user=cls.user)
        cls.test_record.survey.add(cls.test_survey)
        cls.test_evaluator = Assessment.objects.create(evaluator_name='name',evaluator_email='example@mail.com', evaluator_relationship='rel', survey=cls.test_survey, record=cls.test_record)

    def test_evaluator_page(self):     
        response = self._client.get(reverse('view_evaluator', kwargs={'id': self.test_evaluator.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_evaluator.html')
        self.assertEqual(response.context['evaluator'], self.test_evaluator)
        
    def test_edit_evaluator(self):
        response = self._client.post(reverse('edit_evaluator', kwargs={'id':self.test_evaluator.id}), {'name':'new-name', 'email':'new-email', 'rel':'new-rel'})
        self.assertRedirects(response, reverse('view_evaluator', kwargs={'id':self.test_evaluator.id}))
    
    def test_delete_evaluator(self):
        response = self._client.get(f"{reverse('delete_evaluator', kwargs={'id':self.test_evaluator.id})}?next={reverse('view_survey_record', kwargs={'s_id':self.test_survey.id, 'r_id':self.test_record.id})}")
        self.assertRedirects(response, reverse('view_survey_record', kwargs={'s_id':self.test_survey.id, 'r_id':self.test_record.id}))