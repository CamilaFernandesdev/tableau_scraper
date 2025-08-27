# Tableau Scraper

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## O que é?

O **Tableau Scraper** é uma biblioteca Python robusta e flexível para automatizar o download de dados de dashboards do Tableau. Ele utiliza Selenium WebDriver para navegar e interagir com visualizações do Tableau que são exibidas em iframes, oferecendo uma solução confiável para coleta automatizada de dados empresariais.

**Desenvolvido para a Copel (Companhia Paranaense de Energia)**, esta ferramenta facilita a coleta de dados energéticos de fontes como:
- **CCEE** (Câmara de Comercialização de Energia Elétrica)
- **ONS** (Operador Nacional do Sistema Elétrico)
- **ANEEL** (Agência Nacional de Energia Elétrica)

## Características Principais

-  **Automação Inteligente**: Navegação automática e interação com dashboards do Tableau
-  **Configuração Flexível**: Sistema de configuração YAML para diferentes ambientes
-  **Logging Estruturado**: Sistema de logs avançado com suporte a JSON e arquivo
-  **Sistema de Retry**: Tentativas automáticas com configuração de delays
-  **Gerenciamento Automático**: Download automático do ChromeDriver
-  **Context Manager**: Uso seguro com `with` statement
-  **Testes Automatizados**: Suite completa de testes unitários
-  **CLI Integrado**: Interface de linha de comando para uso direto
-  **Integração Airflow**: DAG completo para pipelines de dados

## Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Conexão com internet

### Instalação Básica

```bash
# Clone o repositório
git clone https://github.com/CamilaFernandesdev/tableau_scraper.git
cd tableau_scraper

# Instalação em modo desenvolvimento (recomendado)
pip install -e .
```

### Instalação com Dependências de Desenvolvimento

```bash
# Instala com ferramentas de desenvolvimento
pip install -e ".[dev]"
```

### Instalação via PyPI (quando disponível)

```bash
pip install tableau-scraper
```

## Uso Rápido

### Exemplo Básico

```python
from tableau_scraper import TableauScraper

# Inicializa o scraper
with TableauScraper("https://exemplo.com/dashboard") as scraper:
    # Aceita cookies se necessário
    scraper.accept_cookies('//button[@id="cookies"]')
    
    # Seleciona o dashboard
    scraper.select_tableau_dashboard('.dashboard-selector')
    
    # Interage com elementos
    scraper.find_element('xpath', '//button[@id="download"]')
    
    print("Download concluído!")
```

### Exemplo com Configuração Customizada

```python
from tableau_scraper import TableauScraper

# Usa arquivo de configuração customizado
scraper = TableauScraper(
    url="https://exemplo.com/dashboard",
    view_screen=False,  # Modo headless
    config_path="config.yaml"
)

try:
    # Suas operações aqui
    scraper.accept_cookies('//button[@id="cookies"]')
    scraper.select_tableau_dashboard('.dashboard-selector')
finally:
    scraper.close()
```

## Configuração

### Arquivo de Configuração YAML

Crie um arquivo `config.yaml` para customizar o comportamento:

```yaml
# config.yaml
default:
  chrome:
    driver_path: "/usr/bin/chromedriver"
    headless: true
    timeout: 30
    options:
      - "--no-sandbox"
      - "--disable-dev-shm-usage"
      - "--disable-extensions"
  
  timeouts:
    default_wait: 10
    dashboard_load: 30
    download_wait: 180
  
  retry:
    max_attempts: 3
    delay: 5
  
  logging:
    level: "INFO"
    format: "json"
    file: "tableau_scraper.log"

development:
  chrome:
    headless: false
    timeout: 60
  
  logging:
    level: "DEBUG"
```

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `env.example`:

```bash
# .env
CHROME_DRIVER_PATH=/usr/bin/chromedriver
CHROME_HEADLESS=true
LOG_LEVEL=INFO
```

## API de Referência

### Classe TableauScraper

#### Construtor

```python
TableauScraper(url: str, view_screen: bool = False, config_path: Optional[str] = None)
```

**Parâmetros:**
- `url`: URL da página que contém o dashboard do Tableau
- `view_screen`: Se deve mostrar a tela do Chrome (padrão: False)
- `config_path`: Caminho para arquivo de configuração YAML (opcional)

#### Métodos Principais

##### `accept_cookies(cookies_xpath: str) -> bool`
Aceita cookies automaticamente usando XPath.

```python
success = scraper.accept_cookies('//button[@id="cookies"]')
if success:
    print("Cookies aceitos!")
```

##### `select_tableau_dashboard(css_selector: str) -> bool`
Seleciona o dashboard do Tableau usando CSS Selector.

```python
if scraper.select_tableau_dashboard('.dashboard-class'):
    print("Dashboard selecionado!")
```

##### `find_element(modo: str, localizador: str, timer: int = None) -> bool`
Encontra e clica em elementos usando XPath ou CSS Selector.

```python
# Usando XPath
scraper.find_element('xpath', '//button[@id="download"]')

# Usando CSS Selector
scraper.find_element('css', '.download-button')

# Com tempo de espera customizado
scraper.find_element('xpath', '//button[@id="download"]', 30)
```

##### `select_tableau_rodape() -> bool`
Navega para o rodapé da página e abre o iframe do Tableau.

```python
if scraper.select_tableau_rodape():
    print("Navegou para rodapé com sucesso!")
```

## Interface de Linha de Comando (CLI)

O projeto inclui um CLI para uso direto:

```bash
# Uso básico
tableau-scraper https://exemplo.com/dashboard

# Com configuração customizada
tableau-scraper https://exemplo.com/dashboard --config config.yaml

# Mostrando tela
tableau-scraper https://exemplo.com/dashboard --view-screen

# Com cookies
tableau-scraper https://exemplo.com/dashboard --cookies-xpath '//button[@id="cookies"]'

# Modo verboso
tableau-scraper https://exemplo.com/dashboard --verbose
```

## Testes

### Executando Testes

```bash
# Todos os testes
make test

# Testes com cobertura
make test-cov

# Apenas testes rápidos
make test-fast

# Verificar estilo de código
make lint

# Formatar código
make format
```

### Estrutura de Testes

```
tests/
├── __init__.py
└── test_tableau_scraper.py
```

## Integração com Airflow

O projeto inclui um DAG completo para Apache Airflow, especificamente configurado para a infraestrutura da **Copel**:

```python
# dag.py
from tableau_scraper import TableauScraper

@task
def download_ccee_data(**context):
    with TableauScraper(CCEE_CONFIG['url'], config_path='config.yaml') as scraper:
        # Suas operações aqui
        pass
```

### Tarefas do DAG

1. **download_ccee_data**: Download de dados da CCEE usando Tableau Scraper
2. **process_downloaded_data**: Processamento e limpeza dos dados energéticos
3. **save_to_mongodb**: Salvamento no MongoDB da Copel
4. **upload_to_sharepoint**: Upload para SharePoint da Copel
5. **refresh_powerbi_dataset**: Atualização dos dashboards do PowerBI da Copel
6. **generate_report**: Geração de relatórios para análise energética

## Estrutura do Projeto

```
tableau_scraper/
├── tableau_scraper/          # Código fonte
│   ├── __init__.py
│   ├── tableau_scraper.py    # Classe principal
│   └── cli.py               # Interface de linha de comando
├── tests/                    # Testes automatizados
│   ├── __init__.py
│   └── test_tableau_scraper.py
├── config.yaml              # Configuração YAML
├── env.example              # Exemplo de variáveis de ambiente
├── requirements.txt         # Dependências Python
├── setup.py                # Configuração do pacote
├── pytest.ini             # Configuração do pytest
├── Makefile                # Automação de tarefas
├── dag.py                  # DAG do Apache Airflow
├── script.py               # Script de exemplo
└── README.md               # Esta documentação
```

## Desenvolvimento

### Configuração do Ambiente

```bash
# Clone e configure
git clone https://github.com/CamilaFernandesdev/tableau_scraper.git
cd tableau_scraper

# Instala dependências de desenvolvimento
make dev-setup

# Verifica se tudo está funcionando
make test
```

### Comandos Úteis

```bash
# Ver todos os comandos disponíveis
make help

# Instalar em modo desenvolvimento
make install-dev

# Executar verificações antes do commit
make pre-commit

# Limpar arquivos temporários
make clean

# Construir pacote
make build
```

### Padrões de Código

- **Formatação**: Black
- **Linting**: Flake8
- **Testes**: Pytest
- **Cobertura**: Pytest-cov

## Logs e Monitoramento

### Configuração de Logs

```python
import logging
from tableau_scraper import TableauScraper

# Configura logging
logging.basicConfig(level=logging.INFO)

# Usa o scraper
with TableauScraper("https://exemplo.com") as scraper:
    # Logs são automaticamente gerados
    pass
```

### Formatos de Log

- **Console**: Formato legível para humanos
- **Arquivo**: Formato JSON estruturado
- **Níveis**: DEBUG, INFO, WARNING, ERROR

## Tratamento de Erros

O scraper inclui tratamento robusto de erros:

```python
try:
    with TableauScraper("https://exemplo.com") as scraper:
        if not scraper.accept_cookies('//button[@id="cookies"]'):
            print("Aviso: Cookies não aceitos")
        
        if not scraper.select_tableau_dashboard('.dashboard'):
            raise Exception("Dashboard não encontrado")
            
except Exception as e:
    print(f"Erro: {e}")
```

## Segurança

- **Headless Mode**: Execução sem interface gráfica por padrão
- **Timeout Configurável**: Previne travamentos infinitos
- **Validação de URLs**: Verificação de URLs válidas
- **Isolamento de Processos**: Cada instância é independente

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request


## Agradecimentos

- **Copel** (Companhia Paranaense de Energia) - Pelo suporte e infraestrutura
- Equipe de desenvolvimento da Copel
- **CCEE** - Pela disponibilização dos dados energéticos
- **ONS** - Pelo acesso aos dados do sistema elétrico
- Contribuidores da comunidade open source
- Mantenedores das bibliotecas utilizadas

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Suporte

### Problemas Comuns

1. **ChromeDriver não encontrado**: O scraper baixa automaticamente
2. **Elementos não encontrados**: Verifique seletores XPath/CSS
3. **Timeouts**: Ajuste configurações de timeout no YAML

### Obtendo Ajuda

- [Documentação](https://github.com/CamilaFernandesdev/tableau_scraper/wiki)
- [Issues](https://github.com/CamilaFernandesdev/tableau_scraper/issues)
- [Discussões](https://github.com/CamilaFernandesdev/tableau_scraper/discussions)


---

**Desenvolvido por Camila Fernandes(CamilaFernandesdev) para a Copel**
