import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TableauScraper:

    def __init__(self, url):
        self.URL = url
        self.driver = self.open_chrome()
        self.driver.get(self.URL)
        time.sleep(4)
        print('Entered website')


    def _open_chrome(self):
        """Inicialize the Chrome."""
        options = webdriver.ChromeOptions()
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-session-crashed-bubble")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-web-security")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-infobars")
    
        driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
        return driver

    def accept_cookies(self, cookies_xpath:str):
        """Para aceitar os cookies.
                
        Parameters
        ----------
        cookies_xpath
        
        Steps
        -----
            1. Entre na página e em cima do botão aceitar cookies
            2. Clique com botão direito do mouse e selecione a opção Inspecionar
            3. A localização ficará marcada no DevTools
            4. Clique no botão direito do mouse novamente
            4. E copie o item selecionando na opção XPATH
            
        Examples
        ---------
        Como aparece no DevTools, a seta indica a selecionada:
            <div class="banner-actions-container"> <button id="onetrust-accept-btn-handler">Aceitar todos os cookies</button></div>
        - <button id="onetrust-accept-btn-handler">Aceitar todos os cookies</button>
        
        copiado em xpath:
            //*[@id="onetrust-accept-btn-handler"]
        """
        try:
            cookie_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, cookies_xpath)))
            cookie_btn.click()
            time.sleep(4)
            print('Accepted cookies')
        except:
            print('No cookies banner')

   

    def _open_tableau(self):
        self.driver.switch_to.frame(0)
        time.sleep(4)
        print('Switching to iframe Tableau')
        
    def select_tableau_dashboard(self, css_selector: str):
        self._open_tableau()
        elements = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        elements.click()
        print('Selecting dashboard and waiting downloaded page')
        time.sleep(30)
        
    def select_tableau_rodape(self):
        self.driver.switch_to.default_content()
        self.driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(4)
        self._open_tableau()
        
    def find_element(self, modo: str, localizador: str):
        modo = str().lower().split()
        try:
            if modo=='xpath':
                self.driver.find_element(By.XPATH, localizador).click()
                print('Selecting element in dashboard')
                time.sleep(10)
                
            elif modo=='CSS':
                self.driver.find_element(By.CSS_SELECTOR, localizador).click()
                print('Selecting element in dashboard')
                time.sleep(10)
                
            else:
                print('Forneça um modo de busca: xpath ou css')
                
        except:    
            print('Elements dont finded')
        
        
    # def download_data(self):
    #     self.driver.switch_to.default_content()
    #     self.driver.execute_script("window.scrollBy(0, 800);")
    #     self.timer()
    #     self.driver.switch_to.frame(0)
    #     self.timer()
    #     print('Downloading data')
    #     # icone_download = self.driver.find_element(By
        
    def close(self):
        return self.driver.quit()
        
        
if __name__ == "__main__":
    # Constantes 
    COOKIES_XPATH = "//div[@class='cookie-content d-flex p-3 justify-content-around align-items-center']//button"
    URL = 'https://www.ccee.org.br/web/guest/dados-e-analises/consumo'
    COOKIES_XPATH = '//*[@id="onetrust-accept-btn-handler"]'



    def steps_download_consumo_tableau():
        tableau_scrapper = TableauScrapper()
        tableau_scrapper.go_to_consumo_page()
        tableau_scrapper.download_data()
        tableau_scrapper.close()
