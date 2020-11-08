#task 1

#1. Create code to do next scenario. 
# Acceptance criterias: code can be executed on mentor's pc
# -- Open google 
# -- Seatch for 'selenium install ubuntu python' text
# -- From result search open result that leads you to 'pypi.org'
# -- Find 'selenium' library there('Search projects' field)
# -- Open second result from found items"


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


class GoogleSearchPage(BasePage):
    URL = 'https://www.google.com/'
    
    SEARCH_FIELD = (By.NAME, 'q')
    CITE_PYPI_ORG = (By.PARTIAL_LINK_TEXT, "pypi.org")
    
    def init(self, browser):
        super().init(browser)
        
    def open(self):
        self.browser.get(GoogleSearchPage.URL)
    
    @property
    def search_field(self):
        return self.find_element(GoogleSearchPage.SEARCH_FIELD)
    
    def search_in_google(self, request):
        self.search_field.send_keys(request)
        self.search_field.send_keys(Keys.RETURN)
        
    def open_pypi_org(self):
        self.click(GoogleSearchPage.CITE_PYPI_ORG)

class PupiOrgPage(BasePage):
    URL = 'https://pypi.org/project/selenium/'
    
    SEARCH_FIELD = (By.NAME, 'q')
    
    def init(self, browser):
        super().init(browser)
        
    def open(self):
        self.browser.get(PupiOrgPage.URL)
    
    @property
    def search_field(self):
        return self.find_element(GoogleSearchPage.SEARCH_FIELD)
    
    def search_projects(self, project):
        self.search_field.send_keys(project)
        self.search_field.send_keys(Keys.RETURN)
        

class PupiOrgResultPage(BasePage):
    
    SECOND_RESULT = (By.XPATH, "//*[@aria-label='Search results']//li[2]")
    
    def init(self, browser):
        super().init(browser)
    
    def open(self, by_keyword=None):
        self.browser.get(
            f'https://pypi.org/search/?q={by_keyword}'
            )

        return True
    
    def open_second_result(self):
        self.click(PupiOrgResultPage.SECOND_RESULT)
        

driver = webdriver.Chrome()

googleSearchPage = GoogleSearchPage(driver)
googleSearchPage.open()
googleSearchPage.search_in_google("selenium install ubuntu python")
googleSearchPage.open_pypi_org()

pupiOrgPage = PupiOrgPage(driver)
pupiOrgPage.open()
pupiOrgPage.search_projects("selenium")

pupiOrgResultPage = PupiOrgResultPage(driver)
pupiOrgResultPage.open(by_keyword="selenium")
pupiOrgResultPage.open_second_result()

driver.close()
