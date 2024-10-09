from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from assessment.models import Assessment
from form.models import Form, FormSection, Response
from record.models import Record
from survey.models import Survey


class FormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user= User.objects.create_user(username="username", password="password", email="example@email.com")
        cls._client = Client()
        cls._client.login(username='username', password='password')
        cls.test_form = Form.objects.create(name='name', description='description', user=cls.user)
        cls.test_survey = Survey.objects.create(title='title', form=cls.test_form, email_template='string', user=cls.user)
        cls.test_record = Record.objects.create(first_name='first_name', last_name='last_name', role='role', email='example@mail.com', user=cls.user)
        cls.test_record.survey.add(cls.test_survey)
        cls.test_assessment = Assessment.objects.create(evaluator_name='name', evaluator_email='example@mail.com', evaluator_relationship='rel', record=cls.test_record, survey=cls.test_survey)

    def test_form_creation(self):
        response = self._client.post(reverse('form'), {'name':'name', 'description':'new description'})
        self.assertRedirects(response, reverse('edit_form', kwargs={'id':2}))
    
    def test_form_page(self):
        response = self._client.get(reverse('view_form', kwargs={'id':self.test_form.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertEqual(response.context['form'], self.test_form)
    
    def test_forms_page(self):
        response = self._client.get(reverse('view_forms'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forms.html')
        self.assertQuerySetEqual(response.context['forms'], self.user.form_set.all())

    def test_edit_form_page(self):
        response = self._client.get(reverse('edit_form', kwargs={'id':self.test_form.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit-form.html')
        self.assertEqual(response.context['form'], self.test_form)

    def test_edit_form(self):
        response = self._client.post(reverse('edit_form', kwargs={'id':self.test_form.id}), {'name': 'new name', 'description': 'new description'})
        self.assertRedirects(response, reverse('view_form', kwargs={'id':1}))

    def test_delete_form(self):
        new_form = Form.objects.create(name='new form', description='new description', user = self.user)
        response = self._client.get(reverse('delete_form', kwargs={'id': new_form.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form-delete-success.html')

    def test_add_section(self):
        response = self._client.post(reverse('add_section', kwargs={'id':self.test_form.id}), {'name':'section name', 'question-1':'anxiety'})
        self.assertRedirects(response, reverse('edit_form', kwargs={'id':self.test_form.id}))

    def test_edit_section(self):
        section = FormSection.objects.create(name='delet section', form=self.test_form)
        response = self._client.post(reverse('edit_section', kwargs={'id':section.id}), {'name':'section name', 'new-question-3':'depression'})
        self.assertRedirects(response, reverse('edit_form', kwargs={'id':self.test_form.id}))

    def test_delete_section(self):
        section = FormSection.objects.create(name='delet section', form=self.test_form)
        response = self._client.post(reverse('delete_section', kwargs={'id':section.id}))
        self.assertRedirects(response, reverse('edit_form', kwargs={'id':self.test_form.id}))

    def test_respond_page(self):
        response = self._client.get(reverse('respond', kwargs={'id':self.test_form.id ,'ev_id':self.test_assessment.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'respond.html')
        self.assertEqual(response.context['form'], self.test_form)
        self.assertEqual(response.context['assessment'], self.test_assessment)

    def test_respond(self):
        response = self._client.post(reverse('respond', kwargs={'id':self.test_form.id ,'ev_id':self.test_assessment.id}),{})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thanks-for-responding.html')
        self.assertTrue('response' in response.context)

    def test_view_response(self):
        res = Response.objects.create(form=self.test_form,assessment=self.test_assessment, fields={} )
        response = self._client.get(reverse('response', kwargs={'id':res.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_response.html')
        self.assertEqual(response.context['form'], self.test_form)
        self.assertEqual(response.context['response'], res)