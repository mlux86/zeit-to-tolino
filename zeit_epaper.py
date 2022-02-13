from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class ZeitIssue:
    def __init__(self, driver):
        self.driver = driver

    def get_download_url(self):
        link_elem: WebElement = self.driver.find_element(By.LINK_TEXT, 'EPUB FÜR E-READER LADEN')
        return link_elem.get_attribute('href')


class ZeitEPaper:
    url = 'https://epaper.zeit.de/abo/diezeit/'

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.driver.get(self.url)

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'email').send_keys(username)
        self.driver.find_element(By.NAME, 'pass').send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, 'input[type=\'submit\']').click()
        return self

    def current_issue(self):
        self.driver.find_element(By.LINK_TEXT, 'ZUR AKTUELLEN AUSGABE').click()
        return ZeitIssue(self.driver)
