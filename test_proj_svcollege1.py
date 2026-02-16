from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pytest


@pytest.fixture()
def setup():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get('https://svburger1.co.il/#/HomePage')
    driver.find_element(By.XPATH, '//a[@href = "#/SignIn"]/button').click()
    driver.find_element(By.XPATH, '//input[@placeholder ="Enter your email"]').send_keys("nathan@svcollege.co.il")
    driver.find_element(By.XPATH, '//input[@placeholder ="Enter your password"]').send_keys("Eskimosi")
    driver.find_element(By.XPATH, '//button[@type ="submit"]').click()
    yield driver
    driver.quit()

################################# Sanity #############################################
def test_sanity(setup):
    driver = setup
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//h5[text()="Combo Meal"]')))
    driver.find_element(By.XPATH, '//h5[text()="Combo Meal"]').click()
    driver.find_element(By.XPATH, '//button[contains(text(),"Reserve")]').click()
    driver.find_element(By.XPATH, '//div[@class="col-6"]/button').click()
    assert driver.find_element(By.XPATH, '//h5[text()="Combo Meal"]').is_displayed()
    time.sleep(2)


################################# 1.1. Functionality: order 2 combo meals #############################################
def test_func_order_2_combo(setup):
    driver = setup
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//h5[text()="Combo Meal"]')))
    driver.find_element(By.XPATH, '//h5[text()="Combo Meal"]').click()
    driver.find_element(By.XPATH, '//button[contains(text(),"Reserve")]').click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located
                                    ((By.XPATH, '//input[@index="0"]'))).send_keys(Keys.UP)
    driver.find_element(By.XPATH, '//input[@index="0"]').send_keys(Keys.UP)
    assert driver.find_element(By.XPATH, '//input[@index="0"]').is_displayed()
    time.sleep(2)

################################# 1.2. Functionality: order 1 combo meal, 2 kids meal and 2 burgers ####################
def test_func_order_1_combo_2_kids_2_burgers(setup):
    driver = setup
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//h5[text()="Combo Meal"]')))
    driver.find_element(By.XPATH, '//h5[text()="Combo Meal"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Kids Meal"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Burger"]').click()
    driver.find_element(By.XPATH, '//button[contains(text(),"Reserve")]').click()
    driver.find_element(By.XPATH, '//input[@index="1"]').send_keys(Keys.UP)
    driver.find_element(By.XPATH, '//input[@index="2"]').send_keys(Keys.UP)
    time.sleep(2)
    value_kids = driver.find_element(By.XPATH, '//input[@index="1"]').get_attribute("value")
    value_kids = int(value_kids)
    assert driver.find_element(By.XPATH, '//input[@index="1"]').is_displayed() and value_kids == 2
    time.sleep(2)

    ###################### 1.3. Functionality: Order and cancel 1 Combo Meal, order 1 Kids Meal instead ##################
def test_func_order_1_combo_cancel_1_combo_order_kids(setup):
    driver = setup
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//h5[text()="Combo Meal"]')))
    driver.find_element(By.XPATH, '//h5[text()="Combo Meal"]').click()  # Select 1 Combo Meal
    driver.find_element(By.XPATH, '//h5[text()="Combo Meal"]').click()  # Unselect 1 Combo Meal
    driver.find_element(By.XPATH, '//h5[text()="Kids Meal"]').click()   # Select 1 Kids Meal instead
    # assert driver.find_element(By.XPATH, '//input[@index="1"]').is_displayed()
    assert driver.find_element(By.XPATH, '//h5[text()="Kids Meal"]').is_displayed()
    time.sleep(2)

################################ 2.1 EH: Order over 2 items of same product #################################
def test_EH_order_over_2_items_of_same_product(setup):
    driver = setup
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//h5[text()="Combo Meal"]')))
    driver.find_element(By.XPATH, '//h5[text()="Combo Meal"]').click()
    driver.find_element(By.XPATH, '//button[contains(text(),"Reserve")]').click()
    driver.find_element(By.XPATH, '//input[@index="0"]').send_keys(Keys.UP)
    value_combo = driver.find_element(By.XPATH, '//input[@index="0"]').get_attribute("value")
    value_combo = int(value_combo)
    assert driver.find_element(By.XPATH, '//input[@index="0"]').is_displayed() and value_combo < 3
    time.sleep(2)


################################# 2.2 EH: Order 4 different meals #################################
def test_EH_order_over_3_different_products(setup):
    driver = setup
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//h5[text()="Combo Meal"]')))
    driver.find_element(By.XPATH, '//h5[text()="Combo Meal"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Kids Meal"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Burger"]').click()
    driver.find_element(By.XPATH, '//h5[text()="Vegan"]').click()  # error message: can't choose more than 3 products at the same time
    driver.find_element(By.XPATH, '//button[contains(text(),"Reserve")]').click()
    assert (
            driver.find_element(By.XPATH, '//input[@index="0"]').is_displayed() and
            driver.find_element(By.XPATH, '//input[@index="1"]').is_displayed() and
            driver.find_element(By.XPATH, '//input[@index="2"]').is_displayed()
            )
    time.sleep(2)


