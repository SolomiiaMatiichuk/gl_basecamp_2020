from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def init(self, browser):
        self._browser = browser
        
    @property
    def browser(self):
        if self._browser is None:
            self._browser = webdriver.Chrome()
        else:
            return self._browser
        
    def find_element(self,locators, time = 10):
        try:
            return WebDriverWait(self.browser,time).until(EC.presence_of_element_located((locators)),\
                                            message = f"Can't find element by locator {locators}")
        except TimeoutException:
            self.browser.quit()
        
    
    def click(self, locators, time = 10):
        try: 
            WebDriverWait(self.browser, time).until(EC.visibility_of_element_located((locators)),\
                                            message = f"Can't click on element by locator {locators}")
            self.browser.find_element(*locators).click()
        except TimeoutException:
            self.browser.quit()
      
class GLCareersResultPage(BasePage):

    FIRST_CAREER_PAGELINK = (By.CLASS_NAME, 'career-pagelink')
    
    def init(self, browser):
        super().init(browser)
        
    def getFirst(self):
        return self.find_element(GLCareersResultPage.FIRST_CAREER_PAGELINK)

    def open(self, by_keyword=None):
        self.browser.get(
            f'https://www.globallogic.com/ua/career-search-page/?keywords={by_keyword}&experience=&locations=&c='
            )

        return True        

class GLCareersPage(BasePage):
    URL = 'https://www.globallogic.com/ua/careers/'

    SEARCH_FIELD = (By.ID, 'by_keyword')
    SEARCH_BUTTON = (By.XPATH, '//*[@id="hero"]/div/div/div/div/div/div/div/form/div/button')
    COOKIE_ALLOW_ALL_BUTTON = (By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')

    def init(self, browser):
        super().init(browser)

    
    @property
    def search_field(self):
        return self.find_element(GLCareersPage.SEARCH_FIELD)
        
    def open(self, allow_cookie = True):
        self.browser.get(GLCareersPage.URL)
        if allow_cookie:
            self.click(GLCareersPage.COOKIE_ALLOW_ALL_BUTTON)
        
    def close(self):
        self.browser.close()

    def search_vacancy(self, vacancy, enter=False):
        self.search_field.send_keys(vacancy)
        if enter:
            self.search_field.send_keys(Keys.RETURN)
        else:
            self.click(GLCareersPage.SEARCH_BUTTON)

        return True

    def check_field_exists(self):
        _field = self.search_field

        return _field is not None


# start the browser
driver = webdriver.Chrome()

def test_search_field_exist():
    careersPage = GLCareersPage(driver)
    careersPage.open()

    assert careersPage.check_field_exists(), "Search field is missing"
    

def test_it_can_search():
    careersPage = GLCareersPage(driver)
    careersPage.open(allow_cookie=False)
    careersPage.search_vacancy('QA')

    assert careersPage.check_field_exists(), "Search field is missing"
    
def test_it_can_open_results_page():
    resultPage = GLCareersResultPage(driver)
    assert resultPage.open(by_keyword='')
    
def test_it_can_get_first_element():
    resultPage = GLCareersResultPage(driver)
    resultPage.open(by_keyword='QA')
    assert resultPage.getFirst().text.split("\n")[0] == "Senior QA Automation engineer IRC103517"
