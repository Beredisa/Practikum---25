from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
import time
import pytest

email = "ok.bre@inbox.lv"
password = "beredisa"


# подготавливаем тесты: авторизуемся, заходим на страницу с моими питомцами
@pytest.fixture(scope="module")
def testing_preparation():
    driver = webdriver.Chrome('C:/Driver/chromedriver.exe')
    driver.implicitly_wait(6)
    driver.get('https://petfriends.skillfactory.ru/login')
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(email)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "pass"))).send_keys(password)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    WebDriverWait(driver, 5).until(Ec.element_to_be_clickable((By.XPATH, '//*[@href="/my_pets"]'))).click()

    yield

    driver.quit()


# проверяем, что у меня есть питомцы
def test_I_have_my_pets():
    driver.implicitly_wait(10)
    # проверяем, что у меня есть питомцы
    my_pets = driver.find_elements_by_css_selector('tbody tr')
    if len(my_pets) > 0:
        assert 'I have my pets'
    else:
        Exception('I have not my pets')



# проверяем, что фото есть хотя бы у половины питомцев
def test_half_my_pets_have_photos():
    # получаем фото питомцев
    images = driver.find_elements_by_css_selector('tr th > img')
    # images = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'tr th > img')))
    count = 0
    # проходим циклом по массиву, считаем количество фотографий
    for i in range(len(images)):
        if 'base64' in images[i].get_attribute('src'):
            count += 1
    #  ставим условие по количеству в зависимости от того, четное или нечетное число питомцев (фотографий)
    if (len(images) % 2) == 0:
        assert count >= (len(images) / 2), 'Фото есть у половины питомцев'
    else:
        assert count >= (len(images) / 2 + 1), 'Фото есть более, чем у половины питомцев'


# проверяем, что у всех питомцев есть имя, порода, возраст.
def test_all_my_pets_have_name_type_age():
    info_of_my_pets = driver.find_elements_by_css_selector('tbody td ')
    # info_of_my_pets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tbody td')))
    # получаем имя, породу и возраст питомцев.
    names = info_of_my_pets[::4]
    types = info_of_my_pets[1::4]
    ages = info_of_my_pets[2::4]
    assert '' not in names, 'Не у всех питомцев есть имя'
    # проверяем, что у всех питомцев есть порода
    assert '' not in types, 'Не у всех питомцев есть порода'
    # проверяем, что у всех питомцев есть возраст
    assert '' not in ages, 'Не у всех питомцев есть возраст'

# проверяем имена питомцев
def test_my_pets_different_names():
    info_of_my_pets = driver.find_elements_by_css_selector('tbody td ')
    # info_of_my_pets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tbody td')))
    names = info_of_my_pets[::4]
    assert len(names) == len(list(set(names))), 'У питомцев разные имена'

# проверяем, что у питомцев нет совпадений
def test_different_pets():
    info_of_my_pets = driver.find_elements_by_css_selector('tbody td ')
    # info_of_my_pets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tbody td')))
    # удаляем из списка элементы-крестики (удалить питомца)
    del info_of_my_pets[3::4]
    # группируем каждые три элемента списка питомцев в кортеж (имя,порода,возраст)
    info_of_my_pets_tuple = [tuple(info_of_my_pets[i:i + 3]) for i in range(0, len(info_of_my_pets), 3)]
    # проверяем, есть ли в списке кортежей одинаковые элементы
    assert len(info_of_my_pets_tuple) == len(list(set(info_of_my_pets_tuple))), 'В списке есть повторяющиеся питомцы'

# - путь для теста
# py -m pytest -v --driver Chrome --driver-path chromedriver.exe test_25_5_1.py

