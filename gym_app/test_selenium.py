import pytest
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='module')
def driver():
    """Ініціалізує ChromeDriver один раз на весь модуль"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_client(client, live_server, driver):
    """
    Створює тестового користувача, логінить його через Django-клієнт
    і передає сесію в Selenium WebDriver.
    """
    user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
    client.login(username='testuser', password='testpass123')
    session_cookie = client.cookies['sessionid']
    driver.get(live_server.url)
    driver.add_cookie({'name': 'sessionid', 'value': session_cookie.value, 'path': '/'})
    driver.refresh()
    return driver, live_server.url

def test_dashboard_greeting(logged_in_client):
    """Позитивний тест 1: на головній сторінці є вітання (великі літери)"""
    driver, url = logged_in_client
    driver.get(url)
    greeting = driver.find_element(By.TAG_NAME, 'h2')
    assert 'ПРИВІТ' in greeting.text.upper()
    print("✅ Тест 1 (Dashboard) пройдено")

def test_exercise_form_exists(logged_in_client):
    """Позитивний тест 2: на сторінці вправ присутня форма"""
    driver, url = logged_in_client
    driver.get(f'{url}/exercise/')
    form = driver.find_element(By.TAG_NAME, 'form')
    assert form.is_displayed()
    print("✅ Тест 2 (Форма вправи) пройдено")

def test_missing_element_raises_error(logged_in_client):
    """Негативний тест: шукає неіснуючий елемент (очікувано падає)"""
    driver, url = logged_in_client
    driver.get(f'{url}/exercise/')
    driver.find_element(By.ID, "non-existent-button")