#!/usr/bin/env python3
"""
CLI para o Tableau Scraper
"""

import argparse
import sys
import logging
from pathlib import Path
from tableau_scraper import TableauScraper


def setup_logging(verbose: bool = False) -> None:
    """Configura logging baseado no nível de verbosidade."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def main():
    """Função principal do CLI."""
    parser = argparse.ArgumentParser(
        description="Tableau Scraper - Ferramenta para automatizar downloads do Tableau"
    )
    
    parser.add_argument(
        "url",
        help="URL da página que contém o dashboard do Tableau"
    )
    
    parser.add_argument(
        "--config", "-c",
        help="Caminho para arquivo de configuração YAML"
    )
    
    parser.add_argument(
        "--view-screen", "-v",
        action="store_true",
        help="Mostrar tela do Chrome durante execução"
    )
    
    parser.add_argument(
        "--cookies-xpath",
        help="XPath do botão de aceitar cookies"
    )
    
    parser.add_argument(
        "--dashboard-selector",
        help="CSS Selector do dashboard do Tableau"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Modo verboso (mais logs)"
    )
    
    args = parser.parse_args()
    
    # Configura logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Inicializa o scraper
        logger.info("Iniciando Tableau Scraper")
        scraper = TableauScraper(
            url=args.url,
            view_screen=args.view_screen,
            config_path=args.config
        )
        
        # Aceita cookies se XPath fornecido
        if args.cookies_xpath:
            logger.info("Tentando aceitar cookies")
            if scraper.accept_cookies(args.cookies_xpath):
                logger.info("Cookies aceitos com sucesso")
            else:
                logger.warning("Não foi possível aceitar cookies")
        
        # Seleciona dashboard se selector fornecido
        if args.dashboard_selector:
            logger.info("Selecionando dashboard")
            if scraper.select_tableau_dashboard(args.dashboard_selector):
                logger.info("Dashboard selecionado com sucesso")
            else:
                logger.error("Falha ao selecionar dashboard")
                sys.exit(1)
        
        logger.info("Scraper configurado com sucesso")
        logger.info("Use os métodos do scraper para interagir com o dashboard")
        
        # Mantém o scraper aberto para uso interativo
        if args.view_screen:
            input("Pressione Enter para fechar o scraper...")
        
    except KeyboardInterrupt:
        logger.info("Operação cancelada pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro durante execução: {e}")
        sys.exit(1)
    finally:
        if 'scraper' in locals():
            scraper.close()


if __name__ == "__main__":
    main()
