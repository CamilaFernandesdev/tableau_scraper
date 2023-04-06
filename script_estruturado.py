# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:42:07 2023

@author: E805511
"""

URL = 'https://www.ccee.org.br/web/guest/dados-e-analises/consumo'
COOKIES_XPATH = '//*[@id="alertaCookie"]/div/div[3]/button'
driver = None

try:
    
    import time
    from selenium import webdriver
    from selenium.webdriver import ChromeOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC


    # Entrar no site da CCEE
    #options = Options()
    options = ChromeOptions()
    #options.add_argument("--headless=new")
    # Desativa ro sandbox do navegador, resolve problemas de conexão
    options.add_argument("--no-sandbox")
    # desativa o uso compartilhado de memória IPC entre o processo do navegador e o processo do WebDriver
    options.add_argument("--disable-dev-shm-usage")
    # evitar que o navegador exiba uma mensagem de erro quando ocorrer um erro de sessão.
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
    #options.add_argument('--user-data-dir=/path/to/custom/profile')
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-infobars")

    
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)

    driver.get(URL)
    time.sleep(4)
    print('abri o site')

    # Clica no aceitar os cookies
    # Aceita o banner de cookie (se estiver presente)
    try:
        cookie_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, COOKIES_XPATH)))
        cookie_btn.click()
        time.sleep(4)
    except:
        pass

    print('aceitei os cookies')

    
    time.sleep(10)
    print('teste')
    # Entrar no frame do Tableau
    driver.switch_to.frame(0)
    time.sleep(4)

    # Quarto relatório: download de dados
    painel_download_dados = driver.find_element(By.CSS_SELECTOR, ".tabLastPoint .tabScrollerContentWindow")
    painel_download_dados.click()
    # Geralmente demora para carrdados.click()egar o dashboard
    time.sleep(30)
    print('Estou na quarto relatorio')

    # Retorna para a página principal
    driver.switch_to.default_content()
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(4)
    print('Estou no final da página')
    
    # Retorna para o Tableau
    driver.switch_to.frame(0)
    time.sleep(4)
    print('Retornei para o tableau')
    
    icone_download = driver.find_element(By.CSS_SELECTOR, ".tab-icon-download")
    icone_download.click()
    time.sleep(4)
    print('Estou no ícone de download')
    time.sleep(4)


    # Clica no botão "Tabela de referência cruzada"
    driver.find_element(By.CSS_SELECTOR, ".fdofgby:nth-child(4)").click()
    time.sleep(4)

    # Seleciona a opção CSV
    select_csv = driver.find_element(By.CSS_SELECTOR, ".f81g0pf:nth-child(2)")
    select_csv.click()
    time.sleep(4)

    # Download
    detalhamento_dados = driver.find_element(By.CSS_SELECTOR, ".f7ypqvd")
    detalhamento_dados.click()
    print('Inicio do download')
    time.sleep(180)

except Exception as e:
    print("Ocorreu um erro:", e)

finally:
    if driver is None:
        print('O objeto driver não foi criado corretamente')
       
    else:
         driver.quit()
