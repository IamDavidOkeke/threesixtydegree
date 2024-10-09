from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium import webdriver
from django.contrib.auth.models import User

class ProfileTemplateTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.user= User.objects.create_user(username="username", password="password", email="example@email.com")
        cls.driver.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    # def test_login_page(self):
    #     self.driver.get(f"{self.live_server_url}/login")
    #     username = self.driver.find_element(By.NAME, 'username')
    #     password = self.driver.find_element(By.NAME, 'password')
    #     form = self.driver.find_element(By.TAG_NAME, 'form')
    #     username.send_keys(self.user.username)
    #     password.send_keys(self.user.password)
    #     form.submit()
    #     self.assertTrue(self.user.is_authenticated)

    # def test_register_page(self):
    #     self.driver.get(f"{self.live_server_url}/register")
    #     self.driver.find_element(By.NAME, 'username').send_keys('user')
    #     self.driver.find_element(By.NAME, 'password').send_keys('pass')
    #     self.driver.find_element(By.NAME, 'first_name').send_keys('f_name')
    #     self.driver.find_element(By.NAME, 'last_name').send_keys('l_name')
    #     self.driver.find_element(By.NAME, 'email').send_keys('mail@example.com')
    #     form = self.driver.find_element(By.TAG_NAME, 'form')
    #     form.submit()
    #     self.assertTrue(User.objects.get(username='user'))

    def test_profile_page(self):
        self.client.login(username='username', password='password')
        cookies = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        self.driver.get(f"{self.live_server_url}/profile")
        self.driver.add_cookie({'name':'sessionid', 'value':cookies, 'secure': False, 'path':'/'})
        self.driver.refresh()
        self.driver.get(f"{self.live_server_url}/profile")
        self.assertEqual(self.driver.find_element(By.XPATH, "//*[@data-test-id='profile-link']").get_dom_attribute('href'), f"/profile/")
        self.assertEqual(self.driver.find_element(By.XPATH, "//*[@data-test-id='surveys-link']").get_dom_attribute('href'), f"/survey/all")
        self.assertEqual(self.driver.find_element(By.XPATH, "//*[@data-test-id='forms-link']").get_dom_attribute('href'), f"/form/all")
        self.assertEqual(self.driver.find_element(By.XPATH, "//*[@data-test-id='records-link']").get_dom_attribute('href'), f"/record/all")
        self.assertEqual(self.driver.find_element(By.XPATH, "//*[@data-test-id='logout-link']").get_dom_attribute('href'), f"/logout/")
        self.assertEqual(self.driver.find_element(By.XPATH, "//*[@data-test-id='new-survey-link']").get_dom_attribute('href'), f"/survey/")
        self.assertEqual(self.driver.find_element(By.XPATH, "//*[@data-test-id='new-form-link']").get_dom_attribute('href'), f"/form/")