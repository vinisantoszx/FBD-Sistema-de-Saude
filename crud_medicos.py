import panel as pn
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from urllib.parse import quote_plus

pn.extension(notifications=True)

senha = quote_plus("sebaesses123")
db_url = f'postgresql+pg8000://postgres:{senha}@127.0.0.1:5432/hospital'

engine = create_engine(db_url)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Medico(Base):
    __tablename__ = 'medicos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_completo = Column(String, nullable=False)
    crm = Column(String, unique=True, nullable=False)
    especialidade = Column(String)

Base.metadata.create_all(engine)

input_nome = pn.widgets.TextInput(name='Nome Completo', placeholder='Digite o nome...')
input_crm = pn.widgets.TextInput(name='CRM', placeholder='Digite o CRM...')
input_espec = pn.widgets.TextInput(name='Especialidade', placeholder='Digite a especialidade...')
btn_salvar = pn.widgets.Button(name='Confirmar Cadastro', button_type='primary', icon='device-floppy')

def salvar_medico(event):
    if not input_nome.value or not input_crm.value:
        pn.state.notifications.error("Nome e CRM são obrigatórios!")
        return
        
    session = Session()
    try:
        novo = Medico(
            nome_completo=input_nome.value,
            crm=input_crm.value,
            especialidade=input_espec.value
        )
        session.add(novo)
        session.commit()
        pn.state.notifications.success(f"Médico {input_nome.value} cadastrado!")
        input_nome.value = ""
        input_crm.value = ""
        input_espec.value = ""
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f"Erro: {e}")
    finally:
        session.close()

btn_salvar.on_click(salvar_medico)

layout = pn.Column(
    "# Formulário de Cadastro",
    input_nome, 
    input_crm, 
    input_espec, 
    btn_salvar,
    width=400,
    margin=(20, 20)
)

pn.template.FastListTemplate(
    title="Sistema Hospitalar - Gestão de Médicos",
    main=[layout],
    accent_base_color="#2F4F4F",
    header_background="#2F4F4F",
).servable()