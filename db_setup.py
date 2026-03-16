import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.sqlite import JSON

# Configuração do Banco de Dados
DATABASE_URL = "sqlite:///job_data_pipeline.db"
Base = declarative_base()

class Vaga(Base):
    """Tabela para armazenar os dados principais das vagas (RN-004, RN-006)."""
    __tablename__ = "vagas"

    id = Column(Integer, primary_key=True, index=True)
    url_origem = Column(String, unique=True, nullable=False) # RN-006
    titulo = Column(String, nullable=False)
    empresa = Column(String)
    localizacao = Column(String, nullable=False)
    modalidade = Column(String)
    data_coleta = Column(String, nullable=False)
    # Simulação de JSONB (RN-004) usando TEXT para SQLite
    detalhes_json = Column(Text) 

    def __repr__(self):
        return f"<Vaga(titulo='{self.titulo}', localizacao='{self.localizacao}')>"

class Habilidade(Base):
    """Tabela para armazenar as habilidades extraídas (RF-010)."""
    __tablename__ = "habilidades"

    id = Column(Integer, primary_key=True, index=True)
    vaga_id = Column(Integer, nullable=False) # FK para Vaga
    habilidade = Column(String, nullable=False)
    nivel_senioridade = Column(String) # RF-013

    def __repr__(self):
        return f"<Habilidade(habilidade='{self.habilidade}', vaga_id='{self.vaga_id}')>"

def get_db_engine():
    """Retorna o motor de conexão com o banco de dados."""
    return create_engine(DATABASE_URL)

def setup_database(engine):
    """Cria as tabelas no banco de dados se elas não existirem."""
    Base.metadata.create_all(engine)

def get_db_session(engine):
    """Retorna uma nova sessão de banco de dados."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

if __name__ == "__main__":
    engine = get_db_engine()
    setup_database(engine)
    print(f"Banco de dados SQLite criado em: {DATABASE_URL}")

