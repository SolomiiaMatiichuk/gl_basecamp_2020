#task 2
#2. Create code to do next scenario. 
# Acceptance criterias: You must use explisit waits. code can be executed on mentor's pc
# -- Open 'https://www.globallogic.com/ua/careers/' 
# -- put 'QA' into search field
# -- print to console header of first result"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def init(self, browser):
        self.browser = browser
        
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


class GLCareersPage(BasePage):
    URL = 'https://www.globallogic.com/ua/careers/'

    SEARCH_FIELD = (By.ID, 'by_keyword')
    SEARCH_BUTTON = (By.XPATH, '//*[@id="hero"]/div/div/div/div/div/div/div/form/div/button')
    COOKIE_ALLOW_ALL_BUTTON = (By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
    FIRST_CAREER_PAGELINK = (By.CLASS_NAME, 'career-pagelink')

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

    def print_header_of_first_result(self):
        print(self.find_element(GLCareersPage.FIRST_CAREER_PAGELINK).text)

    
# start the browser
driver = webdriver.Chrome()
        
careersPage = GLCareersPage(driver)
careersPage.open()
careersPage.search_vacancy('QA')
careersPage.print_header_of_first_result()  

driver.close()
