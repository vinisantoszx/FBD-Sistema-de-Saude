import panel as pn
import pandas as pd
from database import SessionLocal, Medico, init_db

init_db()
pn.extension(notifications=True)

input_nome = pn.widgets.TextInput(name='Nome Completo')
input_crm = pn.widgets.TextInput(name='CRM')
input_espec = pn.widgets.TextInput(name='Especialidade')
btn_salvar = pn.widgets.Button(name='Salvar Médico', button_type='primary')

tabela_medicos = pn.widgets.Tabulator(pd.DataFrame(), name='Médicos Cadastrados')

def carregar_dados():
    session = SessionLocal()
    medicos = session.query(Medico).all()
    df = pd.DataFrame([{'ID': m.id, 'Nome': m.nome_completo, 'CRM': m.crm, 'Especialidade': m.especialidade} for m in medicos])
    tabela_medicos.value = df
    session.close()

def salvar_medico(event):
    session = SessionLocal()
    try:
        novo = Medico(nome_completo=input_nome.value, crm=input_crm.value, especialidade=input_espec.value)
        session.add(novo)
        session.commit()
        pn.state.notifications.success("Médico salvo!")
        carregar_dados() 
    except Exception:
        session.rollback()
        pn.state.notifications.error("Erro: CRM já cadastrado ou falha.")
    finally:
        session.close()

btn_salvar.on_click(salvar_medico)

carregar_dados()

template = pn.template.FastListTemplate(
    title="Sistema Hospitalar",
    main=[
        pn.Card(input_nome, input_crm, input_espec, btn_salvar, title="Cadastro"),
        pn.Card(tabela_medicos, title="Médicos Cadastrados")
    ]
)
template.servable()