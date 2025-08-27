"""
Testes unitários para o TableauScraper
"""

import pytest
import tempfile
import yaml
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from tableau_scraper import TableauScraper


class TestTableauScraper:
    """Testes para a classe TableauScraper."""
    
    @pytest.fixture
    def sample_config(self):
        """Configuração de exemplo para testes."""
        return {
            "chrome": {
                "driver_path": "/test/chromedriver",
                "headless": True,
                "timeout": 30,
                "options": ["--no-sandbox", "--headless"]
            },
            "timeouts": {
                "default_wait": 10,
                "dashboard_load": 30,
                "download_wait": 180,
                "cookie_wait": 4,
                "iframe_wait": 4
            },
            "retry": {
                "max_attempts": 3,
                "delay": 5
            },
            "logging": {
                "level": "INFO",
                "format": "json",
                "file": "test.log"
            }
        }
    
    @pytest.fixture
    def temp_config_file(self, sample_config):
        """Arquivo de configuração temporário para testes."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(sample_config, f)
            yield f.name
        Path(f.name).unlink()
    
    @patch('tableau_scraper.tableau_scraper.webdriver.Chrome')
    @patch('tableau_scraper.tableau_scraper.ChromeDriverManager')
    def test_init_with_default_config(self, mock_chrome_manager, mock_chrome_driver):
        """Testa inicialização com configuração padrão."""
        mock_driver = Mock()
        mock_chrome_driver.return_value = mock_driver
        
        with patch('tableau_scraper.tableau_scraper.time.sleep'):
            scraper = TableauScraper("https://example.com")
        
        assert scraper.URL == "https://example.com"
        assert scraper.config is not None
        assert scraper.logger is not None
    
    @patch('tableau_scraper.tableau_scraper.webdriver.Chrome')
    def test_init_with_custom_config(self, mock_chrome_driver, temp_config_file):
        """Testa inicialização com arquivo de configuração customizado."""
        mock_driver = Mock()
        mock_chrome_driver.return_value = mock_driver
        
        with patch('tableau_scraper.tableau_scraper.time.sleep'):
            scraper = TableauScraper("https://example.com", config_path=temp_config_file)
        
        assert scraper.config["chrome"]["driver_path"] == "/test/chromedriver"
    
    def test_load_config_file_not_found(self):
        """Testa carregamento de configuração quando arquivo não existe."""
        scraper = TableauScraper.__new__(TableauScraper)
        config = scraper._load_config("arquivo_inexistente.yaml")
        
        # Deve usar configuração padrão
        assert config["chrome"]["driver_path"] == "/usr/bin/chromedriver"
    
    def test_merge_configs(self):
        """Testa mesclagem de configurações."""
        scraper = TableauScraper.__new__(TableauScraper)
        
        default = {"a": 1, "b": {"c": 2, "d": 3}}
        custom = {"b": {"c": 5}, "e": 6}
        
        result = scraper._merge_configs(default, custom)
        
        assert result["a"] == 1
        assert result["b"]["c"] == 5
        assert result["b"]["d"] == 3
        assert result["e"] == 6
    
    @patch('tableau_scraper.tableau_scraper.webdriver.Chrome')
    def test_open_chrome_with_existing_driver(self, mock_chrome_driver):
        """Testa abertura do Chrome com driver existente."""
        mock_driver = Mock()
        mock_chrome_driver.return_value = mock_driver
        
        scraper = TableauScraper.__new__(TableauScraper)
        scraper.config = {
            "chrome": {
                "driver_path": "/existing/chromedriver",
                "options": ["--no-sandbox"]
            }
        }
        scraper.logger = Mock()
        
        with patch('os.path.exists', return_value=True):
            driver = scraper._open_chrome()
        
        assert driver == mock_driver
    
    @patch('tableau_scraper.tableau_scraper.webdriver.Chrome')
    def test_open_chrome_with_auto_download(self, mock_chrome_driver):
        """Testa abertura do Chrome com download automático do driver."""
        mock_driver = Mock()
        mock_chrome_driver.return_value = mock_driver
        
        scraper = TableauScraper.__new__(TableauScraper)
        scraper.config = {
            "chrome": {
                "driver_path": "/nonexistent/chromedriver",
                "options": ["--no-sandbox"]
            }
        }
        scraper.logger = Mock()
        
        with patch('os.path.exists', return_value=False):
            with patch('tableau_scraper.tableau_scraper.ChromeDriverManager') as mock_manager:
                mock_manager.return_value.install.return_value = "/auto/chromedriver"
                driver = scraper._open_chrome()
        
        assert driver == mock_driver
    
    def test_accept_cookies_success(self):
        """Testa aceitação de cookies com sucesso."""
        scraper = TableauScraper.__new__(TableauScraper)
        scraper.driver = Mock()
        scraper.config = {"retry": {"max_attempts": 3, "delay": 1}, "timeouts": {"default_wait": 10, "cookie_wait": 1}}
        scraper.logger = Mock()
        
        # Mock do WebDriverWait
        mock_wait = Mock()
        mock_element = Mock()
        mock_wait.until.return_value = mock_element
        
        with patch('tableau_scraper.tableau_scraper.WebDriverWait', return_value=mock_wait):
            with patch('tableau_scraper.tableau_scraper.time.sleep'):
                result = scraper.accept_cookies("//button[@id='cookies']")
        
        assert result is True
        mock_element.click.assert_called_once()
    
    def test_accept_cookies_failure(self):
        """Testa falha na aceitação de cookies."""
        scraper = TableauScraper.__new__(TableauScraper)
        scraper.driver = Mock()
        scraper.config = {"retry": {"max_attempts": 3, "delay": 1}, "timeouts": {"default_wait": 10, "cookie_wait": 1}}
        scraper.logger = Mock()
        
        # Mock do WebDriverWait que sempre falha
        mock_wait = Mock()
        mock_wait.until.side_effect = Exception("Timeout")
        
        with patch('tableau_scraper.tableau_scraper.WebDriverWait', return_value=mock_wait):
            with patch('tableau_scraper.tableau_scraper.time.sleep'):
                result = scraper.accept_cookies("//button[@id='cookies']")
        
        assert result is False
    
    def test_context_manager(self):
        """Testa uso como context manager."""
        scraper = TableauScraper.__new__(TableauScraper)
        scraper.close = Mock()
        
        with scraper as s:
            assert s == scraper
        
        scraper.close.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
