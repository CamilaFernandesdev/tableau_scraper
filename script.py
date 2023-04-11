from tableau_scraper import TableauScraper

def tableau_consumo_download_data():
    # CONSTANTES - URL E ELEMENTOS DA TELA
    URL = 'https://www.ccee.org.br/web/guest/dados-e-analises/consumo'
    COOKIES_XPATH = '//*[@id="alertaCookie"]/div/div[3]/button'
    DASHBOARD_DOWNLOAD_DADOS = ".tabLastPoint .tabScrollerContentWindow"
    ICONE_DOWNLOAD = '//*[@id="download-ToolbarButton"]/span[1]'
    TABELA_REFERENCIA_CRUZADA = ".fdofgby:nth-child(4)"
    SELECT_CSV = ".f81g0pf:nth-child(2)"
    DETALHAMENTO_DADOS = ".f7ypqvd"
     
    tableau_scraper = None
    
    try:
        tableau_scraper = TableauScraper(URL, view_screen=True)
        tableau_scraper.accept_cookies(COOKIES_XPATH)
        tableau_scraper.select_tableau_dashboard(DASHBOARD_DOWNLOAD_DADOS)
        tableau_scraper.select_tableau_rodape()
        # click elements tableu
        tableau_scraper.find_element('xpath', ICONE_DOWNLOAD)
        tableau_scraper.find_element('css', TABELA_REFERENCIA_CRUZADA)
        tableau_scraper.find_element('css', SELECT_CSV)
        print('Started download, wait 3 minutes.')
        tableau_scraper.find_element('css', DETALHAMENTO_DADOS, 180)
        
    except Exception as e:
        print('ERROR - ', e)
    
    finally:
        if tableau_scraper is None:
            print('The objeto tableau_scraper não foi criado corretamente')
           
        else:
            tableau_scraper.close()
            print('Chrome closed.')
             

if __name__ == "__main__":
    tableau_consumo_download_data()
