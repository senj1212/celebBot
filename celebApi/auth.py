from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import threading


class Authorization:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.driver = None
        self.session = None
        self.authCheck = False
        self.headers = None
        self.__implementDriver()

    def __implementDriver(self):
        firefox_profile = webdriver.FirefoxProfile()
        self.driver = webdriver.Firefox(executable_path="drivers/geckodriver")
        self.driver.implicitly_wait(8)
        self.wait = WebDriverWait(self.driver, 10)

    def auth(self):
        self.driver.get("https://celeb.tv/login")
        self.driver.find_element(By.CSS_SELECTOR, '[autocomplete=username]').send_keys(self.login)
        self.driver.find_element(By.CSS_SELECTOR, '[autocomplete=password]').send_keys(self.password)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and not(disabled)]"))).click()
        if self.session is None:
            self.session = requests.Session()
        self.waitAuth()

    def waitAuth(self):
        t = threading.Thread(target=self.__waitAuth)
        t.start()

    def __waitAuth(self):
        while not self.authCheck:
            for cookie in self.driver.get_cookies():
                if "authTokenCookie" == cookie['name']:
                    self.session = requests.Session()
                    self.session.cookies["authTokenCookie"] = cookie['value']
                    self.session.headers = {
                        "sec-ch-ua-platform": '"Windows"',
                        "Referer": "https://celeb.tv/",
                        "x-auth-token": cookie['value'],
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.75"
                    }
                    self.authCheck = True
                    break

    def get(self):
        return {
        "driver": self.driver,
        "login": self.login,
        "wite": self.wait,
        "session": self.session,
        }
