import panel as pn
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

pn.extension('tabulator')

engine = create_engine('postgresql+psycopg2://postgres:sebaesses123@localhost:5432/hospital')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Medico(Base):
    __tablename__ = 'medicos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_completo = Column(String, nullable=False)
    crm = Column(String, unique=True, nullable=False)
    especialidade = Column(String)

Base.metadata.create_all(engine)