import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from urllib.parse import quote_plus

load_dotenv()

db_user = os.getenv("DB_USER")
print("O usuário do banco lido é:", db_user)
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

senha = quote_plus(db_pass)
db_url = f'postgresql+pg8000://{db_user}:{senha}@{db_host}:{db_port}/{db_name}'

engine = create_engine(db_url)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

medico_especialidade = Table(
    'medico_especialidade',
    Base.metadata,
    Column('medico_id', Integer, ForeignKey('medicos.id'), primary_key=True),
    Column('especialidade_id', Integer, ForeignKey('especialidades.id'), primary_key=True)
)

class Medico(Base):
    __tablename__ = 'medicos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_completo = Column(String, nullable=False)
    crm = Column(String, unique=True, nullable=False)

    especialidades = relationship("Especialidade", secondary=medico_especialidade, back_populates="medicos")

class Especialidade(Base):
    __tablename__ = 'especialidades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, unique=True, nullable=False)
    
    medicos = relationship("Medico", secondary=medico_especialidade, back_populates="especialidades")

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print("Banco de dados sincronizado!")