import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config


def main():
    """Submit a general fraud report"""
    service = Service(executable_path=config.driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get('https://askedd.edd.ca.gov/AskEDD/s/generalreportfraud?scatN=Report_General_Fraud&parentSubCat=true')

    # Wait for page to load
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'mainContentArea'))
    )

    # What type of fraud are you reporting? Other fraud
    radio_button = driver.find_element(By.XPATH, "//label[@for='radio-2-5']//span[@class='slds-radio_faux']")
    radio_button.click()

    # Is this a new fraud report or an update? New
    radio_button = driver.find_element(By.XPATH, "//label[@for='radio-0-6']//span[@class='slds-radio_faux']")
    radio_button.click()

    # Does your report include identity theft? No
    radio_button = driver.find_element(By.XPATH, "//label[@for='radio-0-7']//span[@class='slds-radio_faux']")
    radio_button.click()

    # Include any details that will help our investigation.
    input_element = driver.find_element(By.XPATH, "//textarea[@id='input-10']")
    input_element.send_keys(config.additional_information)

    # Submit report
    submit_button = driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]")
    submit_button.click()

    time.sleep(10)
    driver.quit()


if __name__ == '__main__':
    main()
