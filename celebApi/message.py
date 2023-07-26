from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep


class MessageManager:
    def __init__(self, session, driver, witeDriver, dbManager):
        self.session = session
        self.driver = driver
        self.driverWite = witeDriver
        self.db = dbManager

    def sendMsg(self, text: str, uid):
        sleep(1)
        self.driver.get(f"https://celeb.tv/chats/{uid}")
        elemInput = self.driver.find_element(By.XPATH, "//input[@placeholder='Type a Message']")
        elemBtnSend = self.driver.find_element(By.XPATH, "//button[(@disabled)]")
        if self.checkLastMsg:
            elemInput.send_keys(text)
            # elemBtnSend.click()
            return True
        return False

    def checkLastMsg(self):
        temporarys = ["just now", "a minute ago", "minute ago", "minutes ago"]
        elements = self.driver.find_elements(By.XPATH, "//p[@class='_2mb60']")
        for temporary in temporarys:
            if temporary in elements[-1].text:
                return False
        return True
