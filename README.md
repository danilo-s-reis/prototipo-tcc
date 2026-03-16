# Protótipo de Pipeline de Análise de Vagas de TI

Este projeto é um protótipo em Python que implementa uma pipeline de **E**xtração, **T**ransformação e **C**arga (**ETL**) com um módulo de **P**rocessamento de **L**inguagem **N**atural (**PLN**) e um **Dashboard** interativo, conforme os requisitos e regras de negócio fornecidos.

## Arquitetura e Tecnologias

O protótipo foi construído com base na seguinte arquitetura modular, utilizando as tecnologias Python:

| Módulo | Tecnologias | Requisitos Atendidos |
| :--- | :--- | :--- |
| **Simulação de Web Scraping** | `requests`, `BeautifulSoup` (simulados) | RF-001, RF-002, RF-003, RNF-003, RNF-005, RNF-008 |
| **ETL (Transformação)** | `pandas`, Expressões Regulares (`re`) | RF-004, RF-005, RF-007 |
| **Persistência (Carga)** | `SQLAlchemy`, `sqlite3` | RF-006, RN-004, RN-006, RNF-001 |
| **Análise de Dados (PLN)** | Python puro, Dicionário de Habilidades | RF-008, RF-009, RF-010, RN-005 |
| **Visualização (Dashboard)** | `Streamlit`, `Plotly Express` | RF-011 a RF-015, RNF-002, RNF-007 |

## Estrutura do Projeto

*   `main.py`: Contém a lógica da pipeline ETL e do módulo PLN. É o ponto de entrada para a coleta e processamento de dados.
*   `db_setup.py`: Define o esquema do banco de dados (tabelas `vagas` e `habilidades`) e as funções de conexão com o `sqlite3`.
*   `dashboard.py`: Implementa o painel de visualização interativo usando Streamlit.
*   `job_data_pipeline.db`: O banco de dados SQLite gerado após a execução do `main.py`.
*   `requirements.txt`: Lista de dependências Python.

## Como Executar o Protótipo

### 1. Configuração do Ambiente

As dependências necessárias estão listadas no `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 2. Execução da Pipeline ETL e PLN

Execute o script principal para simular a coleta, processar os dados e popular o banco de dados:

```bash
python3 main.py
```

Esta etapa irá:
1.  Criar o arquivo `job_data_pipeline.db`.
2.  Simular a extração de dados de vagas.
3.  Limpar e normalizar os dados (ETL).
4.  Aplicar o módulo PLN para extrair habilidades e senioridade.
5.  Persistir os dados nas tabelas `vagas` e `habilidades`.

### 3. Visualização do Dashboard

O dashboard interativo pode ser iniciado com o Streamlit:

```bash
streamlit run dashboard.py
```

O dashboard estará acessível no seu navegador, geralmente em `http://localhost:8501`.

## Implementação dos Requisitos

| Requisito | Descrição | Implementação no Protótipo |
| :--- | :--- | :--- |
| **RF-001, RF-002** | Extração de dados da vaga e descrição completa. | Simulado em `main.py` com dados de amostra. |
| **RF-005** | Limpeza e normalização de dados. | Função `normalize_data` em `main.py` (Ex: "S. Paulo" para "São Paulo"). |
| **RF-007** | Uso da biblioteca `pandas` para ingestão. | Uso de `df.to_sql` em `main.py`. |
| **RF-008, RF-009, RF-010** | PLN para extração de habilidades. | Função `run_pln_module` em `main.py` com dicionário de habilidades. |
| **RF-011 a RF-015** | Dashboard com indicadores e gráficos. | Implementado em `dashboard.py` usando Streamlit e Plotly. |
| **RN-004** | Esquema de banco de dados híbrido (JSONB). | Simulado em `db_setup.py` usando o tipo `TEXT` para armazenar JSON serializado. |
| **RN-006** | URL de origem como campo único. | Restrição `unique=True` na coluna `url_origem` da tabela `vagas` em `db_setup.py`. |
| **RNF-003, RNF-005** | Técnicas anti-detecção (atrasos, User-Agents). | Simulado e comentado na função `simulate_web_scraping` em `main.py`. |
| **RNF-006** | Código modular e documentado. | Projeto dividido em `main.py`, `db_setup.py` e `dashboard.py`. |

