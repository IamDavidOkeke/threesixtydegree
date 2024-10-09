from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from assessment.helpers import email_body_template
from form.models import Form
from record.models import Record
from survey.models import Survey

class SurveyCreationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user= User.objects.create_user(username="username", password="password", email="example@email.com")
        cls._client = Client()
        cls._client.login(username='username', password='password')
        cls.test_form = Form.objects.create(name='name', description='description', user=cls.user)
    
    def test_survey_creation_page(self):
        response = self._client.get(reverse('survey'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_survey.html')
        self.assertTrue('forms' in response.context)

    def test_survey_creation(self):
        response = self._client.post(reverse('survey'), {'title':'title', 'form':self.test_form.id, 'email-template':email_body_template})
        self.assertRedirects(response, reverse('view_survey', kwargs={'id':1}))

class SurveyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user= User.objects.create_user(username="username", password="password", email="example@email.com")
        cls._client = Client()
        cls._client.login(username='username', password='password')
        cls.test_form = Form.objects.create(name='name', description='description', user=cls.user)
        cls.test_survey = Survey.objects.create(title='title', form=cls.test_form, email_template=email_body_template, user=cls.user)

    def test_survey_page(self):     
        response = self._client.get(reverse('view_survey', kwargs={'id': self.test_survey.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'survey.html')
        self.assertEqual(response.context['survey'], self.test_survey)
        
    def test_surveys_page(self):
        response = self._client.get(reverse('view_surveys'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_surveys.html')
        self.assertQuerySetEqual(Survey.objects.filter(user=self.user), response.context['surveys'], ordered=False)
    
    def test_add_new_record_to_survey(self):
        response = self._client.post(f"{reverse('add_record', kwargs={'id':self.test_survey.id})}?type=new", {"first_name": "first_name","last_name": "last_name", "role": "role", "email":"example@email.com"})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [{"model": "record.record", "pk": 1, "fields": {"first_name": "first_name", "last_name": "last_name", "email": "example@email.com", "role": "role"}}])
    
    def test_add_existing_record_to_survey(self):
        record = Record.objects.create(first_name='first_name', last_name='last_name', role='role', email='example@mail.com', user=self.user)
        response = self._client.post(f"{reverse('add_record', kwargs={'id':self.test_survey.id})}?type=existing", {"record_id":record.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [{"model": "record.record", "pk": 1, "fields": {"first_name": "first_name", "last_name": "last_name", "email": "example@mail.com", "role": "role"}}])
    
class TestSurveyRecord(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user= User.objects.create_user(username="username", password="password", email="example@email.com")
        cls._client = Client()
        cls._client.login(username='username', password='password')
        cls.test_form = Form.objects.create(name='name', description='description', user=cls.user)
        cls.test_survey = Survey.objects.create(title='title', form=cls.test_form, email_template=email_body_template, user=cls.user)
        cls.test_record = Record.objects.create(first_name='first_name', last_name='last_name', role='role', email='example@mail.com', user=cls.user)
        cls.test_record.survey.add(cls.test_survey)
    
    def test_view_survey_record(self):
        response = self._client.get(reverse('view_survey_record', kwargs={'s_id':self.test_survey.id, 'r_id':self.test_record.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_survey_record.html')
        self.assertEqual(response.context['record'], self.test_record)
        self.assertEqual(response.context['survey'], self.test_survey)
    
    def test_add_evaluator(self):
        response = self._client.post(reverse('add_evaluator', kwargs={'s_id':self.test_survey.id, 'r_id':self.test_record.id}), {'name':'name', 'email':'example@mail.com', 'rel':'rel'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [{"model": "assessment.assessment", "pk": response.json()[0]['pk'], "fields": {"evaluator_name": "name", "evaluator_email": "example@mail.com", "evaluator_relationship": "rel"}}])

    def test_delete_record_from_survey(self):
        response = self._client.get(reverse('delete_survey_record', kwargs={'s_id':self.test_survey.id, 'r_id':self.test_record.id}))
        self.assertRedirects(response, reverse('view_survey', kwargs={'id':self.test_survey.id}))