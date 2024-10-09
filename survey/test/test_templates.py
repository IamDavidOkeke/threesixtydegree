from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium import webdriver
from django.contrib.auth.models import User
from assessment.models import Assessment
from form.models import Form
from record.models import Record
from survey.models import Survey

class SurveyTemplateTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.user= User.objects.create_user(username="username", password="password", email="example@email.com")
        cls.driver.implicitly_wait(10)
        cls.client = Client()
        cls.client.login(username='username', password='password')
        cookies = cls.client.cookies[settings.SESSION_COOKIE_NAME].value
        cls.driver.get(f"{cls.live_server_url}")
        cls.driver.add_cookie({'name':'sessionid', 'value':cookies, 'secure': False, 'path':'/'})
        cls.driver.refresh()
        cls.driver.get(f"{cls.live_server_url}")
        cls.test_form = Form.objects.create(name='name', description='description', user=cls.user)
        cls.test_survey = Survey.objects.create(title='title', form=cls.test_form, user=cls.user)
        cls.test_record = Record.objects.create(first_name='first_name', last_name='last_name', role='role', email='example@mail.com', user=cls.user)
        cls.test_record.survey.add(cls.test_survey)
        cls.test_evaluator = Assessment.objects.create(evaluator_name='name',evaluator_email='example@mail.com', evaluator_relationship='rel', survey=cls.test_survey, record=cls.test_record)

    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def get_elem(self, id):
        return self.driver.find_element(By.XPATH, f"//*[@data-test-id='{id}']")
    
    def get_elems(self, id):
        return self.driver.find_elements(By.XPATH, f"//*[@data-test-id='{id}']")


    def test_view_survey(self):
        self.driver.get(f"{self.live_server_url}{reverse('view_survey', kwargs={'id':self.test_survey.id})}")
        self.assertEqual(self.get_elem('survey-title').text, self.test_survey.title)
        self.assertEqual(self.get_elem('form-name').text, self.test_survey.form.name)
        template_records = self.get_elems('survey-record')
        self.assertEqual(len(template_records), self.test_survey.record_set.all().count())
        self.get_elem('existing-record-btn').click()
        self.assertEqual(len(self.get_elems('non-survey-record')), Record.objects.filter(user=self.user).exclude(survey=self.test_survey).count())
        self.get_elem('add-record-btn').click()
        new_record_form = self.get_elem('new-record-form')
        new_record_form.find_element(By.NAME, 'first_name').send_keys('a')
        new_record_form.find_element(By.NAME, 'last_name').send_keys('a')
        new_record_form.find_element(By.NAME, 'email').send_keys('a')
        new_record_form.find_element(By.NAME, 'role').send_keys('a')
        self.driver.execute_script('return submit_record()')
        self.assertEqual(len(self.get_elems('survey-record')), len(template_records)+1)
        self.assertEqual(self.test_survey.record_set.all().count(), len(self.get_elems('survey-record')))

    def test_view_surveys(self):
        self.driver.get(f"{self.live_server_url}{reverse('view_surveys')}")
        self.assertEqual(self.user.survey_set.all().count(), len(self.get_elems('survey')))
    
    def test_view_survey_record(self):
        self.driver.get(f"{self.live_server_url}{reverse('view_survey_record', kwargs={'s_id':self.test_survey.id,'r_id':self.test_record.id})}")
        self.assertEqual(self.get_elem('title').text, f'{self.test_record.first_name} {self.test_record.last_name} for {self.test_survey.title}')
        old_eval = self.get_elems('evaluator')
        self.assertEqual(self.test_record.assessment_set.filter(survey=self.test_survey).count(), len(old_eval))
        self.assertEqual(self.get_elem('record-link').get_dom_attribute('href'), reverse('record', kwargs={'id':self.test_record.id}))
        self.assertEqual(self.get_elem('remove-record-link').get_dom_attribute('href'), reverse('delete_survey_record',  kwargs={'s_id':self.test_survey.id,'r_id':self.test_record.id}))
        self.get_elem('open-modal-btn').click()
        new_eval_form = self.get_elem('new-eval-form')
        new_eval_form.find_element(By.NAME, 'name').send_keys('a')
        new_eval_form.find_element(By.NAME, 'email').send_keys('a')
        new_eval_form.find_element(By.NAME, 'rel').send_keys('a')
        self.driver.execute_script('return submit()')
        self.assertEqual(len(self.get_elems('evaluator')), len(old_eval)+1)
        self.assertEqual(self.test_record.assessment_set.filter(survey=self.test_survey).count(), len(self.get_elems('evaluator')))

    def test_survey_creation(self):
        self.driver.get(f"{self.live_server_url}{reverse('survey')}")
        old_survey_count = self.user.survey_set.all().count()
        new_eval_form = self.get_elem('survey-form')
        new_eval_form.find_element(By.NAME, 'title').send_keys('a title')
        self.get_elems('form')[0].click()
        self.get_elem('mail-template-btn').click()
        new_eval_form.find_element(By.NAME, 'mail-template').send_keys('a template')
        self.driver.execute_script('return submit()')
        self.assertEqual(self.user.survey_set.all().count() - old_survey_count, 1)
        self.assertEqual(self.user.survey_set.all()[old_survey_count].title, 'a title')
