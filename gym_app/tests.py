import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class GymSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        # Створимо тестового користувача
        from django.contrib.auth.models import User
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.client.login(username='testuser', password='testpass')
        # Отримаємо сесію для Selenium
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url)
        self.driver.add_cookie({'name': 'sessionid', 'value': cookie.value, 'path': '/'})
        self.driver.refresh()

    def test_login_and_dashboard(self):
        """Позитивний тест: перевіряє, що після входу бачимо головну сторінку"""
        self.driver.get(self.live_server_url)
        heading = self.driver.find_element(By.TAG_NAME, 'h2')
        self.assertIn('Привіт', heading.text)
        print("✅ Тест 1 (Dashboard) пройдено")

    def test_exercise_form_displayed(self):
        """Позитивний тест: форма додавання вправи відображається"""
        self.driver.get(f'{self.live_server_url}/exercise/')
        form = self.driver.find_element(By.TAG_NAME, 'form')
        self.assertTrue(form.is_displayed())
        print("✅ Тест 2 (Форма вправи) пройдено")

    def test_nonexistent_element_fails(self):
        """Негативний тест: шукає неіснуючий елемент (очікувано падає)"""
        self.driver.get(f'{self.live_server_url}/exercise/')
        # Елемент з id="non-existent-button" відсутній
        self.driver.find_element(By.ID, "non-existent-button")
        self.fail("Тест мав впасти, але елемент знайшовся!")