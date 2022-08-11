from multiprocessing import context
from random import shuffle
from time import sleep, time
from requests import options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import selenium
import os
import os.path
import sys
import tkinter.messagebox
import json

TIMEOUT_WAIT = 10
ORDER_FILE_NAME = "order.json"
APP_FOLDER = "."

pathToApp = __file__
while not pathToApp.endswith('.app'):
    if pathToApp == "/":
        break
    pathToApp = os.path.dirname(pathToApp)

if pathToApp != "/":
    APP_FOLDER = os.path.dirname(pathToApp)

def click_item(item):
    for x in range(3):
        try:
            item.click()
            break
        except selenium.common.exceptions.ElementNotInteractableException:
            sleep(1)
        except selenium.common.exceptions.ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", item)
            return

def find_button_with_text(driver, text):
    return WebDriverWait(driver, timeout=TIMEOUT_WAIT).until(lambda d: d.find_element(By.XPATH,f'//button[.//*[text()="{text}"]]'))

def orderItem(driver, item_name, options={}, quantity=1):
    button = WebDriverWait(driver, timeout=TIMEOUT_WAIT).until(lambda d: d.find_element(By.XPATH,f'//button[.//h4[text()="{item_name}"]]'))
    click_item(button)

    addToCartButton = WebDriverWait(driver, timeout=TIMEOUT_WAIT).until(lambda d: d.find_element(By.XPATH,f'//button[@data-anchor-id="AddToCartButton"]'))

    for option in options:
        checkboxes = driver.find_elements(By.XPATH, f'//div[@aria-labelledby="optionList_{option}"]//input[@type="checkbox"]')
        for checkbox in checkboxes:
            if checkbox.is_selected():
                click_item(checkbox)

        label = driver.find_element(By.XPATH, f'//div[@aria-labelledby="optionList_{option}"]//label[.//*[text()="{options[option]}"]]')
        click_item(label)

    if quantity > 1:
        increase_button = driver.find_element(By.XPATH, '//button[@aria-label="Increase quantity by 1"]')
        for x in range(quantity - 1):
            click_item(increase_button)

    
    addToCartButton.click()
    WebDriverWait(driver, timeout=TIMEOUT_WAIT).until_not(lambda d: d.find_element(By.XPATH, '//*[@role="dialog"]'))

def checkout(driver, shouldOrder):
    checkout_button = WebDriverWait(driver, timeout=TIMEOUT_WAIT).until(lambda d: d.find_element(By.PARTIAL_LINK_TEXT, "Checkout"))
    driver.execute_script("arguments[0].click();", checkout_button)

    if shouldOrder:
        place_order_button = WebDriverWait(driver, timeout=TIMEOUT_WAIT).until(lambda d: d.find_element(By.XPATH,f'//button[.//*[text()="Place Order"]]'))
        click_item(place_order_button)
        # TODO quit after seeing confirmation page
        # driver.quit()

def checkLogin(driver):

    try:
        signInButtons = WebDriverWait(driver, timeout=2).until(lambda d: d.find_elements(By.XPATH, '//*[text()[contains(.,"Sign In")]]'))
    except selenium.common.exceptions.TimeoutException:
        return
    if len(signInButtons) > 0:  
        parent = tkinter.Tk() # Create the object
        parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
        parent.withdraw()

        answer = tkinter.messagebox.askokcancel('BagelOrder: Not Signed In', 'The user is not signed into DoorDash, please sign and set the delivery location and then click OK on this dialog. Clicking "Cancel" will exit the order script')
        if answer:
            checkLogin(driver)
        else:
            driver.quit()
            sys.exit(0)

def set_address(driver, address):
    address_popup_button = driver.find_element(By.XPATH, '//button[@aria-controls="layout-address-picker"]')
    click_item(address_popup_button)

    address_bar = WebDriverWait(driver, timeout=TIMEOUT_WAIT).until(lambda d: d.find_element(By.XPATH,f'//input[@placeholder="Address"]'))
    address_bar.clear()
    address_bar.send_keys(address)
    sleep(0.5)
    address_bar.send_keys(Keys.ENTER)

    save_button = find_button_with_text(driver, "Save")
    click_item(save_button)

    WebDriverWait(driver, timeout=TIMEOUT_WAIT).until_not(lambda d: d.find_element(By.XPATH, '//div[@data-testid="AddressEditForm"]'))

def try_clear_menu_button(text):
    try:
        view_menu_button = WebDriverWait(driver, timeout=2).until(lambda d: d.find_element(By.XPATH,f'//button[.//*[text()="{text}"]]'))
        click_item(view_menu_button)
    except selenium.common.exceptions.TimeoutException:
        pass

def clear_cart(driver):
    buttons = driver.find_elements(By.XPATH, '//button[@data-anchor-id="RemoveOrderCartItemButton"]')
    for button in buttons:
        click_item(button)

def set_time(driver, day_string, time_string):
    time_button = driver.find_element(By.XPATH, '//button[@aria-controls="layout-time-picker"]')
    click_item(time_button)

    day_button = WebDriverWait(driver, timeout=TIMEOUT_WAIT).until(lambda d: d.find_element(By.XPATH,f'//button[.//*[text()="{day_string}"]]'))
    click_item(day_button)

    time_string = time_string.replace('-', '–')
    time_string = time_string.replace(' ', ' ')
    hour_button = WebDriverWait(driver, timeout=TIMEOUT_WAIT).until(lambda d: find_button_with_text(d, time_string))
    click_item(hour_button)

    WebDriverWait(driver, timeout=TIMEOUT_WAIT).until_not(lambda d: d.find_element(By.ID, "layout-time-picker"))

def run_order(driver, order):
    driver.get(order["site"])

    try_clear_menu_button("See Menu")
    try_clear_menu_button("View Menu")

    checkLogin(driver)
    set_address(driver, order['address'])
    set_time(driver, order["day"], order["time"])
    
    try_clear_menu_button("View Menu")

    clear_cart(driver)

    for item in order['items']:
        orderItem(driver, item['name'], item['options'], item['quantity'])

    checkout(driver, shouldOrder=True)

import contextlib
import logging

fh = logging.FileHandler('/tmp/logger.log')
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.addHandler(fh)
LOGGER.setLevel(logging.WARNING)
with open('/tmp/error.txt', 'w') as log:
    with contextlib.redirect_stderr(log):
        with contextlib.redirect_stdout(log):
            with open(os.path.join(APP_FOLDER, ORDER_FILE_NAME)) as order_file:
                chrome_options = Options() 
                chrome_options.add_argument(f'--user-data-dir={os.path.expanduser("~")}/Library/Application Support/Google/Chrome/BagelOrder')
                chrome_options.add_experimental_option("detach", True)

                service = Service(executable_path=ChromeDriverManager().install())

                driver = webdriver.Chrome(service=service, options=chrome_options)

                orders = json.load(order_file)
                for order in orders:
                    run_order(driver, order)

