import time
import random
import re
import json
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from db_setup import Vaga, Habilidade, get_db_engine, setup_database

# --- 1. Módulo de Extração de Dados (Web Scraping - Simulado) ---
def simulate_web_scraping():
    """
    Simula a extração de dados de vagas (RF-001, RF-002).
    A simulação inclui dados brutos e uma descrição HTML para o módulo ETL processar (RF-004).
    """
    print("Iniciando simulação de Web Scraping...")
    
    # Simulação de técnicas anti-detecção e atrasos (RNF-003, RNF-005)
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    ]
    
    # Simulação de diferentes tipos de paginação (RF-003)
    # A implementação real exigiria 'requests' ou 'selenium'
    
    raw_data = [
        {
            "url_origem": "https://vagas.com/vaga/1",
            "titulo": "Desenvolvedor Python Pleno/Sênior",
            "empresa": "TechCorp",
            "localizacao_bruta": "São Paulo - SP (Remoto)",
            "html_descricao": "<html><body><h1>Descrição da Vaga</h1><p>Estamos buscando um **Desenvolvedor Python** com experiência em **Django** e **PostgreSQL**. Conhecimento em **AWS** é um diferencial. **Requisitos:** 5 anos de experiência. Modalidade: **Remoto**.</p><ul><li>Uso de **Pandas** para ETL.</li><li>Experiência com **Docker**.</li></ul></body></html>"
        },
        {
            "url_origem": "https://vagas.com/vaga/2",
            "titulo": "Analista de Dados Júnior",
            "empresa": "DataSolutions",
            "localizacao_bruta": "Rio de Janeiro/RJ",
            "html_descricao": "<html><body><p>Vaga para Analista de Dados. Necessário conhecimento em **SQL** e ferramentas de BI como **Power BI**. Desejável familiaridade com **R** para análise estatística. Local: **Presencial**.</p></body></html>"
        },
        {
            "url_origem": "https://vagas.com/vaga/3",
            "titulo": "Engenheiro de Software Sênior",
            "empresa": "GlobalSoft",
            "localizacao_bruta": "S. Paulo",
            "html_descricao": "<html><body><p>Procuramos Engenheiro Sênior. Foco em microsserviços com **Java** e **Spring Boot**. Experiência com **Kubernetes** e metodologias **Agile**. Modalidade: **Híbrido**.</p></body></html>"
        }
    ]
    
    # Simulação de atraso aleatório (RNF-003)
    time.sleep(random.uniform(1, 3))
    print(f"Coletadas {len(raw_data)} vagas simuladas.")
    
    return raw_data

# --- 2. Módulo de Transformação e Carga (ETL) ---

def normalize_data(raw_data):
    """
    Limpa e normaliza os dados extraídos (RF-005, RF-004).
    Retorna um DataFrame Pandas (RF-007).
    """
    print("Iniciando Transformação de Dados...")
    
    processed_data = []
    
    for item in raw_data:
        # RF-004: Extrair texto da descrição HTML
        soup = BeautifulSoup(item["html_descricao"], "lxml")
        descricao_texto = soup.get_text(separator=" ", strip=True)
        
        # RF-005: Padronização de Localização e Modalidade
        local_bruto = item["localizacao_bruta"]
        localizacao = local_bruto.replace("S. Paulo", "São Paulo").replace("/RJ", "").replace(" - SP", "").strip()
        
        # Tentativa de extrair modalidade
        modalidade = "Presencial"
        if "Remoto" in local_bruto or "Remoto" in descricao_texto:
            modalidade = "Remoto"
        elif "Híbrido" in descricao_texto:
            modalidade = "Híbrido"
            
        # RN-004: Preparar dados para o esquema híbrido
        detalhes = {
            "descricao_completa": descricao_texto,
            "html_original": item["html_descricao"]
        }
        
        processed_data.append({
            "url_origem": item["url_origem"],
            "titulo": item["titulo"],
            "empresa": item["empresa"],
            "localizacao": localizacao,
            "modalidade": modalidade,
            "data_coleta": datetime.now().strftime("%Y-%m-%d"),
            "detalhes_json": json.dumps(detalhes) # JSON serializado para TEXT
        })
        
    df = pd.DataFrame(processed_data)
    print(f"Transformação concluída. DataFrame com {len(df)} linhas.")
    return df

def load_data(df, engine):
    """
    Carrega os dados processados na tabela 'vagas' (RF-006, RF-007, RNF-001).
    Utiliza a ingestão em lote do Pandas para otimização.
    """
    print("Iniciando Carga de Dados (Load)...")
    
    # Ingestão em lote usando Pandas to_sql (RF-007, RNF-001)
    # if_exists='append' garante que novos dados sejam adicionados.
    # index=False evita a escrita do índice do DataFrame como uma coluna.
    # chunksize ajuda na otimização de grandes volumes de dados.
    try:
        df.to_sql(
            name='vagas', 
            con=engine, 
            if_exists='append', 
            index=False, 
            chunksize=1000,
            # Para lidar com a restrição UNIQUE (RN-006), a implementação real
            # exigiria um merge/upsert, mas para o protótipo simples, vamos
            # apenas tentar inserir e tratar o erro de unicidade (se o SQLite suportasse).
            # No SQLite, a maneira mais simples de simular o RN-006 é garantir que 
            # o DataFrame não tenha duplicatas antes de tentar a inserção, mas
            # o SQLAlchemy/Pandas com SQLite não suporta UPSERT nativamente.
            # Vamos confiar na restrição UNIQUE definida na classe Vaga.
        )
        print(f"Carga de {len(df)} registros na tabela 'vagas' concluída.")
    except Exception as e:
        # Em um ambiente real com PostgreSQL, usaríamos 'method=multi' ou uma 
        # função de upsert para lidar com duplicatas (RN-006).
        print(f"Erro durante a carga de dados: {e}. Alguns registros podem ter sido duplicados ou ignorados.")
        print("Continuando o protótipo...")

def run_pln_module(engine):
    """
    Executa o módulo de Processamento de Linguagem Natural (PLN) para extrair habilidades.
    (RF-008, RF-009, RF-010, RN-005)
    """
    print("\nIniciando Módulo de PLN...")
    
    # Dicionário de Habilidades (RF-009, RN-005)
    # Lista simplificada para o protótipo
    habilidades_dict = [
        "Python", "Django", "PostgreSQL", "AWS", "Pandas", "Docker", 
        "SQL", "Power BI", "R", "Java", "Spring Boot", "Kubernetes", "Agile"
    ]
    
    # Mapeamento de termos de senioridade para normalização (RF-013)
    senioridade_map = {
        "júnior": "Júnior",
        "junior": "Júnior",
        "pleno": "Pleno",
        "sênior": "Sênior",
        "senior": "Sênior"
    }

    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 1. Recuperar todas as vagas do banco de dados
    vagas = session.query(Vaga).all()
    
    habilidades_para_inserir = []
    
    for vaga in vagas:
        # 2. Extrair a descrição completa do JSON (RN-004)
        detalhes = json.loads(vaga.detalhes_json)
        descricao = detalhes.get("descricao_completa", "")
        
        # 3. Normalizar o texto para PLN
        texto_normalizado = descricao.lower()
        
        # 4. Extração de Habilidades (RF-008, RF-009)
        habilidades_encontradas = set()
        for habilidade in habilidades_dict:
            if habilidade.lower() in texto_normalizado:
                habilidades_encontradas.add(habilidade)
                
        # 5. Extração de Nível de Senioridade (RF-013)
        senioridade_encontrada = "Não Especificado"
        for termo, nivel in senioridade_map.items():
            if termo in vaga.titulo.lower() or termo in texto_normalizado:
                senioridade_encontrada = nivel
                break
        
        # 6. Preparar para inserção na tabela 'habilidades' (RF-010)
        for habilidade in habilidades_encontradas:
            habilidades_para_inserir.append(Habilidade(
                vaga_id=vaga.id,
                habilidade=habilidade,
                nivel_senioridade=senioridade_encontrada
            ))

    # 7. Inserção em lote na tabela 'habilidades'
    session.bulk_save_objects(habilidades_para_inserir)
    session.commit()
    session.close()
    
    print(f"PLN concluído. {len(habilidades_para_inserir)} habilidades extraídas e persistidas.")


def run_etl_pipeline():
    """Executa a pipeline ETL completa."""
    engine = get_db_engine()
    setup_database(engine) # Garante que as tabelas existam
    
    raw_data = simulate_web_scraping()
    df_vagas = normalize_data(raw_data)
    load_data(df_vagas, engine)
    
    return engine

if __name__ == "__main__":
    engine = run_etl_pipeline()
    run_pln_module(engine)
    print("\nPipeline ETL e PLN (simuladas) concluídas com sucesso.")

