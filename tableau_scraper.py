
"""
Tableau geralmente usa uma técnica chamada "embbeding" para exibir suas visualizações.
O que significa que as visualizações são exibidas em um iframe separado em vez de diretamente
no código HTML da página.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TableauScraper:
    
    def __init__(self, modo= 'tradicional'| 'servidor'):
        """Inicialize the Chrome."""
        if 'tradicional':
            self.driver = webdriver.Chrome()
        elif 'servidor':
            options = Options()
            self.driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
            time.sleep(20)
        else:
            print('Escolha uma das opções de modo: tradicional ou servidor')
            

    def accept_cookies(self, cookies_xpath: str):
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
        except:
            pass

    def go_to_page(self, url: str, cookies_xpath: str):
        self.driver.get(url)
        time.sleep(4)
        self.accept_cookies(cookies_xpath)
        time.sleep(4)
        self.driver.maximize_window()
        time.sleep(4)
        
        
    def switch_tableau(self):
        self.driver.switch_to.frame(0)
        time.sleep(4)

    def find_elements_css(self,localizador: str):
        try:
            if modos=='xpath':
                self.driver.find_element(By.XPATH, localizador)
                time.sleep(40)
            elif modos=='CSS':
                self.driver.find_element(By.CSS_SELECTOR, localizador)
                time.sleep(40)
            else:
                print('')
        except:    
            pass
    def return_page(self):
        self.driver.switch_to.default_content()
        time.sleep(4)

    def download_data(self):
        self.switch_to_iframe(0)
        painel_download_dados = self.driver.find_element(By.CSS_SELECTOR, ".tabLastPoint .tabScrollerContentWindow")
        painel_download_dados.click()
        time.sleep(30)
        self.switch_to_default_content()
        self.driver.execute_script("window.scrollBy(0, 800);")
        self.switch_to_iframe(0)
        icone_download = self.driver.find_element(By.CSS_SELECTOR, ".tab-icon-download")
        icone_download.click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".fdofgby:nth-child(4)").click()
        time.sleep(1)
        select_csv = self.driver.find_element(By.CSS_SELECTOR, ".f81g0pf:nth-child(2)")
        select_csv.click()
        time.sleep(1)
        detalhamento_dados = self.driver.find_element(By.CSS_SELECTOR, ".f7ypqvd")
        detalhamento_dados.click()
        time.sleep(130)

    def close(self):
        self.driver.quit()
   

if __name__ == "__main__":
    # Constantes 
    COOKIES_XPATH = "//div[@class='cookie-content d-flex p-3 justify-content-around align-items-center']//button"
    URL = 'https://www.ccee.org.br/web/guest/dados-e-analises/consumo'



def steps_download_consumo_tableau():
    tableau_scrapper = TableauScrapper()
    tableau_scrapper.go_to_consumo_page()
    tableau_scrapper.download_data()
    tableau_scrapper.close()
