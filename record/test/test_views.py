from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from record.models import Record


class RecordCreationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user= User.objects.create_user(username="username", password="password", email="example@email.com")
        cls._client = Client()
        cls._client.login(username='username', password='password')

    def test_record_creation_page(self):
        response = self._client.get(reverse('create_record'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_record.html')

    def test_record_creation(self):
        response = self._client.post(reverse('create_record'), {"first_name": "first_name","last_name": "last_name", "role": "role", "email":"example@email.com"})
        self.assertRedirects(response, reverse('record', kwargs={'id':1}))

class RecordPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="username", password="password", email="example@mail.com")        
        cls.test_record = Record(first_name='first_name', last_name='last_name', role='role', email='example@mail.com', user=cls.user)
        cls.test_record.save()
        cls._client = Client()
        cls._client.login(username='username', password='password')

    def test_record_page(self):     
        response = self._client.get(reverse('record', kwargs={'id': self.test_record.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'record.html')
        self.assertEqual(response.context['record'], self.test_record)
        
    def test_records_page(self):
        response = self._client.get(reverse('records'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records.html')
        self.assertQuerySetEqual(Record.objects.filter(user=self.user), response.context['records'], ordered=False)
    
    def test_edit_record(self):
        response = self._client.post(reverse('edit_record', kwargs={'id': self.test_record.id}), {"first_name": "first_name","last_name": "last_name", "role": "role", "email":"example@email.com"})
        self.assertRedirects(response, reverse('record', kwargs={'id':self.test_record.id}))

    def test_delete_record(self):
        response = self._client.get(f"{reverse('delete_record', kwargs={'id': self.test_record.id})}?next={reverse('records')}")
        self.assertRedirects(response, reverse('records'))