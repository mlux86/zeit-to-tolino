from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class ThaliaLogin:
    LOGIN_URL = 'https://www.thalia.de/auth/oauth2/authorize?client_id=webreader&response_type=code&scope=SCOPE_BOSH&redirect_uri=https%3A%2F%2Fwebreader.mytolino.com%2Flibrary%2F&x_buchde.skin_id=17&x_buchde.mandant_id=2'

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.driver.get(self.LOGIN_URL)

    def login(self, username, password):
        self.driver.find_element(By.ID, 'j_username').send_keys(username)
        self.driver.find_element(By.ID, 'j_password').send_keys(password)
        self.driver.find_element(By.NAME, 'login').click()

        self.driver.find_element(By.CSS_SELECTOR, 'div[data-test-id=\'ftu-country-de-DE\']').click()
        self.driver.find_element(By.CSS_SELECTOR, 'div[data-test-id=\'ftu-resellerLogo-3\']').click()

        return ThaliaLibrary(self.driver)


class ThaliaLibrary:
    SECONDS_WAIT_UPLOAD = 10

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.driver.find_element(By.CSS_SELECTOR, 'span[data-test-id=\'library-drawer-MyBooks\']').click()

    def get_num_entries(self):
        return len(self.driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id=\'library-myBooks-titles-list\'] > div > div'))

    def upload(self, file_path):
        num_entries = self.get_num_entries() # which is also the max index to wait for
        upload = self.driver.find_element(By.CSS_SELECTOR, 'input[type=\'file\']')
        upload.send_keys(file_path)
        WebDriverWait(self.driver, self.SECONDS_WAIT_UPLOAD)\
            .until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, f'span[data-test-id=\'library-myBooks-titles-list-{num_entries}-title\']')))
