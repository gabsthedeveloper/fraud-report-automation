import time
from datetime import date

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config


def fill_out_first_page(driver):
    """Fill out report's first page: report type"""
    # Wait for page to load
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'mainContentArea'))
    )

    # Is this a new fraud report or an update? New
    radio_button = driver.find_element(By.XPATH, "//label[@for='radio-0-5']//span[@class='slds-radio_faux']")
    radio_button.click()

    # Does your report include identity theft? No
    radio_button = driver.find_element(By.XPATH, "//label[@for='radio-1-6']//span[@class='slds-radio_faux']")
    radio_button.click()

    # To which EDD program does your report relate? Unemployment
    dropdown_button = driver.find_element(By.XPATH, "//button[@id='combobox-button-8']")
    dropdown_button.click()
    dropdown_option = driver.find_element(By.XPATH, "//span[@class='slds-truncate'][normalize-space()='Unemployment']")
    dropdown_option.click()

    # Are you an employer? No
    radio_button = driver.find_element(By.XPATH, "//label[@for='radio-1-12']//span[@class='slds-radio_faux']")
    radio_button.click()

    # Continue to next page
    continue_button = driver.find_element(By.XPATH, "//button[@title='Continue']")
    continue_button.click()


def fill_out_second_page(driver):
    """Fill out report's second page: suspect's information"""
    # Wait for page to load
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'mainContentArea'))
    )

    # First Name
    input_element = driver.find_element(By.XPATH, "//input[@id='input-17']")
    input_element.send_keys(config.suspect['first_name'])

    # Last Name
    input_element = driver.find_element(By.XPATH, "//input[@id='input-21']")
    input_element.send_keys(config.suspect['last_name'])

    # Gender
    dropdown_button = driver.find_element(By.XPATH, "//button[@id='combobox-button-27']")
    dropdown_button.click()
    dropdown_option = driver.find_element(By.XPATH, f"//span[@class='slds-truncate'][normalize-space()='{config.suspect['gender']}']")
    dropdown_option.click()

    # City
    input_element = driver.find_element(By.XPATH, "//input[@id='input-33']")
    input_element.send_keys(config.suspect['city'])

    # Approximate Age
    approximate_birth_year = config.suspect['approximate_birth_year']
    if approximate_birth_year:
        input_element = driver.find_element(By.XPATH, "//input[@id='input-49']")
        approximate_age = date.today().year - approximate_birth_year
        input_element.send_keys(approximate_age)

    # What leads you to believe the person is committing fraud?
    input_element = driver.find_element(By.XPATH, "//textarea[@id='input-51']")
    input_element.send_keys(config.fraud_reason)

    # Is there any additional information you would like to provide?
    input_element = driver.find_element(By.XPATH, "//textarea[@id='input-105']")
    input_element.send_keys(config.additional_information)

    # Continue to next page
    continue_button = driver.find_element(By.XPATH, "//button[@title='Continue']")
    continue_button.click()


def main():
    """Submit a unemployment fraud report"""
    service = Service(executable_path=config.driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get('https://askedd.edd.ca.gov/AskEDD/s/reportfraud?scatN=Report_Unemployment_Fraud&parentSubCat=true')

    # fill out report pages
    fill_out_first_page(driver)
    fill_out_second_page(driver)
    # Leave third page blank to remain anonymous

    # Submit report
    submit_button = driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]")
    submit_button.click()

    time.sleep(10)
    driver.quit()


if __name__ == '__main__':
    main()
