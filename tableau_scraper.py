"""
Tableau geralmente usa uma técnica chamada "embbeding" para exibir suas visualizações.
O que significa que as visualizações são exibidas em um iframe separado em vez de diretamente
no código HTML da página.
"""

import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TableauScraper:
    def __init__(self, url, view_screen=False):
        """
        Initialize the TableauScraper class.
        
        Parameters
        ----------
        url : str
            URL of the webpage to be scraped.
        view_screen : bool, optional
            Whether to show the screen when running or not, by default False.
        """
        self.URL = url
        self.driver = self._open_chrome(view_screen)
        self.driver.get(self.URL)
        time.sleep(10)
        print('Entered website')


    def _open_chrome(self, view_screen=False):
        """
        Open Chrome using Selenium WebDriver.
        
        Parameters
        ----------
        view_screen : bool, optional
            Whether to show the screen when running or not, by default False.
        
        Returns
        -------
        WebDriver
            A Chrome WebDriver object.
        """
        options = ChromeOptions()
        
        if view_screen == False:
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

    def accept_cookies(self, cookies_xpath:str) -> None:
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
            5. E copie o item selecionando na opção XPATH
            
        Examples
        ---------
        Como aparece no DevTools, a linha selecionada:
         - <button id="onetrust-accept-btn-handler">Aceitar todos os cookies</button>
        
        copiado em xpath ficará assim:
            //*[@id="onetrust-accept-btn-handler"]
        """
        try:
            cookie_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, cookies_xpath)))
            cookie_btn.click()
            time.sleep(4)
            print('Accepted cookies')
        except:
            print('No cookies banner or button dont found')

   

    def _open_tableau(self):
        """Switches to Tableau iframe."""
        self.driver.switch_to.frame(0)
        time.sleep(4)
        print('Switching to iframe Tableau')
        
    def select_tableau_dashboard(self, css_selector: str):
        """
        Method to select the Tableau dashboard.

        Parameters
        ----------
        css_selector : str
            The CSS Selector of the Tableau dashboard on the website.

        Returns
        -------
        None

        """
        self._open_tableau()
        elements = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        elements.click()
        print('Selecting dashboard and waiting downloaded page')
        time.sleep(30)
        
    def select_tableau_rodape(self):
        self.driver.switch_to.default_content()
        print('Switching to principal page')
        self.driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(4)
        self._open_tableau()
        
    def find_element(self, modo: str, localizador: str, timer=10) -> None:
        """
        Method to find and select an element on a Tableau dashboard.

        Parameters
        ----------
        modo : str
            The search method to use: 'xpath' or 'css'.
        localizador : str
            The locator for the desired element.
        timer : int, optional
            The number of seconds to wait after selecting the element, by default 10 secs.

        Returns
        -------
        None
        """
        modo = str(modo).lower().strip()
        try:
            if modo == 'xpath':
                element = self.driver.find_element(By.XPATH, localizador)
                element.click()
                print('Selecting element in dashboard')
                time.sleep(timer)
                
            elif modo =='css':
                element = self.driver.find_element(By.CSS_SELECTOR, localizador)
                element.click()
                print('Selecting element in dashboard')
                time.sleep(timer)
                
            else:
                print('Forneça um modo de busca: xpath ou css' \
                      'ou não é posssível localizar o elemento(ícone).') 
                
        except :    
            print('Elements dont found')
        
        
    def close(self):
        """Quits the webdriver."""
        return self.driver.quit()
        
    
