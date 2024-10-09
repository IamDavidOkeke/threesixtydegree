from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium import webdriver
from django.contrib.auth.models import User
from assessment.models import Assessment
from form.models import Form, FormSection, InputField, InputTextField, Response, TextFieldResponse
from record.models import Record
from survey.models import Survey

class FormTemplateTest(StaticLiveServerTestCase):
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
        cls.test_section = FormSection.objects.create(name='section', form=cls.test_form)
        cls.test_section2 = FormSection.objects.create(name='section2', form=cls.test_form)
        cls.test_question = InputField.objects.create(label='label', section=cls.test_section)
        cls.test_question2 = InputField.objects.create(label='label', section=cls.test_section2)
        cls.test_text_question = InputTextField.objects.create(label='label',  form=cls.test_form)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def get_elem(self, id):
        return self.driver.find_element(By.XPATH, f"//*[@data-test-id='{id}']")
    
    def get_elems(self, id):
        return self.driver.find_elements(By.XPATH, f"//*[@data-test-id='{id}']")
    
    def test_create_template(self):
        self.driver.get(f"{self.live_server_url}{reverse('form')}")
        old_form_count = self.user.form_set.all().count()
        new_form = self.get_elem('new-form')
        new_form.find_element(By.NAME, 'name').send_keys('form name')
        new_form.find_element(By.NAME, 'description').send_keys('form description')
        self.assertEqual(self.get_elem('submit-btn').get_dom_attribute('type'), 'submit')
        new_form.submit()
        self.assertEqual(self.user.form_set.all().count() - old_form_count, 1)
        self.assertEqual(self.user.form_set.all()[old_form_count].name, 'form name')
    
    def test_view_form_template(self):
        form = self.test_form
        self.driver.get(f"{self.live_server_url}{reverse('view_form', kwargs={'id':form.id})}")
        self.assertEqual(self.get_elem('name').text, form.name)
        self.assertEqual(self.get_elem('description').text, form.description)
        sections = self.get_elems('section')
        self.assertEqual(len(sections), form.formsection_set.all().count())
        for s in sections:
            db_section = FormSection.objects.get(pk=s.get_dom_attribute('id'))
            self.assertEqual(s.find_element(By.TAG_NAME, 'h3').text, db_section.name)
            questions = s.find_elements(By.XPATH, f".//*[@data-test-id='question']")
            self.assertEqual(len(questions), db_section.inputfield_set.all().count())
            for q in questions:
                self.assertEqual(q.text, InputField.objects.get(pk=q.get_dom_attribute('id')).label)
        text_question = self.get_elems('text-question')
        self.assertEqual(len(text_question), form.inputtextfield_set.all().count())
        for t in text_question:
            self.assertEqual(t.find_element(By.TAG_NAME, 'label').text, InputTextField.objects.get(pk=t.get_dom_attribute('id')).label)
        self.assertEqual(self.get_elem('edit-link').get_dom_attribute('href'), reverse('edit_form', kwargs={'id':form.id}))
        self.assertEqual(self.get_elem('delete-link').get_dom_attribute('href'), reverse('delete_form', kwargs={'id':form.id}))
        
    def test_view_forms(self):
        self.driver.get(f"{self.live_server_url}{reverse('view_forms')}")
        self.assertEqual(self.user.form_set.all().count(), len(self.get_elems('form')))
        self.assertEqual(self.get_elem('create-link').get_dom_attribute('href'), reverse('form'))
    
    def test_edit_form(self):
        form = self.test_form
        self.driver.get(f"{self.live_server_url}{reverse('edit_form', kwargs={'id':form.id})}")
        meta = self.get_elem('meta-form')
        self.assertEqual(meta.find_element(By.NAME, 'name').get_dom_attribute('value'), form.name)
        self.assertEqual(meta.find_element(By.NAME, 'description').text, form.description)
        sections = self.get_elems('section')
        self.assertEqual(len(sections), form.formsection_set.all().count())
        for s in sections:
            db_section = FormSection.objects.get(pk=s.get_dom_attribute('id'))
            self.assertEqual(s.find_element(By.TAG_NAME, 'h3').text , db_section.name)
            self.assertEqual(s.find_element(By.XPATH, f".//*[@data-test-id='edit-btn']").get_dom_attribute('onclick'), f"edit_section('{s.get_dom_attribute('id')}')")
            self.assertEqual(s.find_element(By.XPATH, f".//*[@data-test-id='delete-link']").get_dom_attribute('href'), reverse('delete_section', kwargs={'id':s.get_dom_attribute('id')}))
            self.driver.execute_script(' edit_section(arguments[0])', s.get_dom_attribute('id'))
            edit_form = self.get_elem(f"form-{s.get_dom_attribute('id')}")
            questions = edit_form.find_elements(By.XPATH, f".//*[@data-test-id='question']")
            self.assertEqual(len(questions), db_section.inputfield_set.all().count())
            for q in questions:
                self.assertEqual(q.find_element(By.TAG_NAME, 'input').get_dom_attribute('value'), InputField.objects.get(pk=q.get_dom_attribute('id')).label)
                self.assertEqual(q.find_element(By.TAG_NAME, 'button').get_dom_attribute('onclick'), f'delete_field("{q.get_dom_attribute('id')}")')
        
    def test_add_section(self):
        db_form = self.test_form
        old_count = db_form.formsection_set.all().count()
        self.driver.get(f"{self.live_server_url}{reverse('edit_form', kwargs={'id':db_form.id})}")
        self.driver.execute_script("edit_section('new')")
        form = self.get_elem('add-section-form')
        form.find_element(By.NAME,'name').send_keys('section name')
        self.driver.execute_script("add_field('question')")
        form.find_element(By.XPATH,f".//*[@data-test-id='question']").send_keys('question name')
        form.submit()
        new_sections = db_form.formsection_set.all()
        self.assertEqual(new_sections.count(),old_count+1)
        self.assertEqual(new_sections[old_count].name, 'section name')
        self.assertEqual(new_sections[old_count].inputfield_set.all().count(), 1)
        self.assertEqual(new_sections[old_count].inputfield_set.all()[0].label, 'question name')