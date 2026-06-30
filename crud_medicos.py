from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from urllib.parse import quote_plus

senha = quote_plus("sebaesses123")
db_url = f'postgresql+pg8000://postgres:{senha}@127.0.0.1:5432/hospital'

engine = create_engine(db_url)
Base = declarative_base()

class Medico(Base):
    __tablename__ = 'medicos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_completo = Column(String, nullable=False)
    crm = Column(String, unique=True, nullable=False)
    especialidade = Column(String)

Base.metadata.create_all(engine)
print("Tabela 'medicos' criada com sucesso!")


Session = sessionmaker(bind=engine)
session = Session()

novo_medico = Medico(nome_completo="Dr. Teste", crm="12345", especialidade="Clínico Geral")

session.add(novo_medico)
session.commit()
print("Médico inserido com sucesso!")