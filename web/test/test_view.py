from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class IndexTest(SimpleTestCase):
    def test_index(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class RegisterTest(TestCase):
    def test_registration_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_registration(self):
        response = self.client.post(reverse('register'), {"username": "username", "password": "password", "email":"example@email.com", "first_name":"first_name", "last_name":"last_name"})
        self.assertRedirects(response, reverse('login'))

class LoginTest(TestCase):
    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_pass(self):
        user = User.objects.create_user(username="username", password="password", email="example@email.com")
        response = self.client.post(reverse('login'), {"username":"username", "password":"password"})
        self.assertRedirects(response, reverse('profile'))

    
class LogoutTest(TestCase):
    def setUp(self):
        self.user= User.objects.create_user(username="username", password="password", email="example@email.com").save()

    def test_logout(self):
        self.client.login(username="username", password="password")
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

class ProfileTest(TestCase):
    def setUp(self):
        self.user= User.objects.create_user(username="username", password="password", email="example@email.com").save()

    def test_profile(self):
        self.client.login(username="username", password="password")
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')