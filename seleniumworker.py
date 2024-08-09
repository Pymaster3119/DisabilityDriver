import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service;
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support import expected_conditions as EC
import re
import time

options = Options()
options.set_preference("profile", "/Users/aditya/Desktop/DisabledDriver/o0fvibos.Adblock Profile")
driver = webdriver.Firefox(options=options, service=Service(executable_path = os.path.realpath("geckodriver")))
driver.set_window_size(1000,1000)

def clickElement(identifier):
    identified = False
    trials = [By.ID, By.CLASS_NAME, By.CSS_SELECTOR, By.LINK_TEXT, By.PARTIAL_LINK_TEXT, By.TAG_NAME, By.XPATH]
    for i in trials:
        try:
            elements = driver.find_elements(i, identifier)
            for element in elements:
                try:
                    actionchain = ActionChains(driver,duration=2)
                    actionchain.move_to_element(to_element=element)
                    actionchain.click()
                    actionchain.perform()
                    identified = True
                    break
                except:
                    pass
        except Exception as e:
            print(e)
    if not identified:
        print(identifier)
        raise Exception("Element not found")
    
def type(text, questions):
    actionchain = ActionChains(driver)
    if "answer" in text:
        match = re.search(r'question\d+', text)
        text = questions[match.group(0)]
    actionchain.send_keys(text)
    actionchain.perform()

def press(button):
    if button.lower() == "enter":
        actionchain = ActionChains(driver)
        actionchain.send_keys(Keys.RETURN)
        actionchain.perform()

def clickintelligent(exp, questions):
    eval(exp)