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
import re
import time
driver = webdriver.Firefox(service=Service(executable_path = os.path.realpath("geckodriver")))
driver.set_window_size(1000,1000)

#Install adblock (THANK GOD!)
driver.get("https://addons.mozilla.org/en-US/firefox/addon/adblock-for-firefox/")
time.sleep(1)
driver.find_element(By.CLASS_NAME, "Button Button--action AMInstallButton-button Button--puffy").click()
driver.switch_to.alert.accept()

def clickElement(identifier):
    identified = False
    trials = [By.CLASS_NAME, By.CSS_SELECTOR, By.ID, By.LINK_TEXT, By.PARTIAL_LINK_TEXT, By.TAG_NAME, By.XPATH]
    for i in trials:
        try:
            element = driver.find_element(i, identifier)
            actionchain = ActionChains(driver,duration=1)
            actionchain.move_to_element(to_element=element)
            for i in range(100):
                actionchain.click()
            actionchain.perform()
            identified = True
        except:
            pass
    if not identified:
        print("NADA")
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
    #That's all it took :O
    eval(exp)