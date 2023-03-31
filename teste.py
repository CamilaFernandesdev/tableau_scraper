# -*- coding: utf-8 -*-
"""
Tableau geralmente usa uma técnica chamada "embbeding" para exibir suas visualizações, 
o que significa que as visualizações são exibidas em um iframe separado em vez de diretamente
no código HTML da página.


"""


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def timer(seg=4):
    return time.sleep(seg)

# Entrar no site da CCEE
driver = webdriver.Chrome()
driver.get('https://www.ccee.org.br/web/guest/dados-e-analises/consumo')
timer()


# Clica no aceitar os cookies
# Aceita o banner de cookie (se estiver presente)
try:
    cookie_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='cookie-content d-flex p-3 justify-content-around align-items-center']//button")))
    cookie_btn.click()
    timer()
except:
    pass


# Tela FullScreen
driver.maximize_window()
timer()
driver.execute_script("document.body.style.zoom='50%'")
timer()

# Para clicar em um elemento dentro de uma visualização do Tableau
# alternar para o iframe onde a visualização está sendo exibida antes de localizar e clicar no elemento
driver.switch_to.frame(0)
timer()

painel_download_dados = driver.find_element(By.CSS_SELECTOR, ".tabLastPoint .tabScrollerContentWindow")
painel_download_dados.click()
# Geralmente demora para carregar o dashboard
timer(30)
print('deu certo')



driver.switch_to.default_content()
driver.execute_script("window.scrollBy(0, 800);")
timer()
driver.switch_to.frame(0)

timer()
icone_download = driver.find_element(By.CSS_SELECTOR, ".tab-icon-download")
icone_download.click()
timer()

#actions.move_to_element(icone_download).click().perform()
#icone_download.click()
print('agora vai')
timer()


# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# test = '//*[@id="download-ToolbarButton"]'
# icone_download_rodape = driver.find_element(By.XPATH, test)
# timer()
# actions = ActionChains(driver)
# actions.move_to_element(icone_download_rodape).click().perform()
# print('testando')
# timer()



# a = driver.find_element(By.CSS_SELECTOR, ".fdofgby:nth-child(4)").click()
# timer()
# b = driver.find_element(By.CSS_SELECTOR, ".f81g0pf:nth-child(2)").click()
# timer()

# timer()
# c = driver.find_element(By.CSS_SELECTOR, ".f7ypqvd").click()
# timer(240)

# driver.quit()

# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# driver.switch_to.default_content()

# Literalmente mover o mouse para clicar no elemento
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# timer()
# driver.switc

# driver.execute_script("arguments[0].scrollIntoView();", icone_download_rodape)
# icone_download_rodape.click()
# print('testando')
# timer(15)




# icone_download_rodape = driver.find_element(By.XPATH, test)
# icone_download_rodape.click()
timer(15)


# # Espera até que o botão correspondente ao quarto dashboard seja visível na página
# path_tableau = 'tabStoryPointContent tab-widget'
# xpath_tableau = '//*[@id="tabZoneId4"]/div/div/div/span[2]/div/span/span/span[4]/div[2]/div/div[1]/span/div'
# path_tableau2 ='<div class="tableauPlaceholder" id="viz1677178621121" style="position: relative; width: 1124px; height: 895px; overflow: hidden; display: block;'

# timer()
# dashboard_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_tableau)))
# timer()
# dashboard_btn.click()
# =============================================================================
# EGGEA
# DOWNLOAD_DADOS = '//*[@id="tabZoneId4"]/div/div/div/span[2]/div/span/span/span[4]/div[2]/div/div[1]/span/div'
# timer()
# # Clica na div com o texto "Clique aqui"
# div_clicar_aqui = driver.find_element_by_xpath("//div[contains(text(), 'download de dados')]")
# div_clicar_aqui.click()

# # Encontra a posição da visualização do Tableau na página
# pos_x, pos_y = pag.locateCenterOnScreen('tableau.png')
# pag.click(pos_x, pos_y)

# # try:
#     img = pag.locateCenterOnScreen('xxxxxxxxx', confidence=0.7)
    
    
# except:
#     time.sleep(1)
#     print('Não encontrado - Download de Dados Tableau')
    
