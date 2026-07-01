import panel as pn
import pandas as pd
from database import SessionLocal, Medico, Especialidade, init_db

init_db()
pn.extension(notifications=True)

pn.config.raw_css.append("""
    body, .main, .card { background-color: #ffffff !important; color: #000000 !important; }
    .tabulator { background-color: #ffffff !important; }
    .tabulator-cell { white-space: normal !important; word-wrap: break-word !important; }
""")

input_nome = pn.widgets.TextInput(name='Nome Completo', sizing_mode='stretch_width')
input_crm = pn.widgets.TextInput(name='CRM', sizing_mode='stretch_width')
input_especs = pn.widgets.MultiChoice(name='Especialidades', options=[e.nome for e in SessionLocal().query(Especialidade).all()], sizing_mode='stretch_width')
input_id = pn.widgets.TextInput(name='ID', visible=False)

btn_salvar = pn.widgets.Button(name='Salvar Médico', button_type='primary')
btn_deletar = pn.widgets.Button(name='Remover Selecionado', button_type='danger')
btn_editar = pn.widgets.Button(name='Editar Selecionado', button_type='warning')

container_tabela = pn.Column()

def carregar_dados():
    session = SessionLocal()
    medicos = session.query(Medico).all()
    dados = []
    for m in medicos:
        nomes = sorted(list(set([e.nome for e in m.especialidades])))
        dados.append({'ID': m.id, 'Nome': m.nome_completo, 'CRM': m.crm, 'Especialidade': ", ".join(nomes)})
    
    df = pd.DataFrame(dados, columns=['ID', 'Nome', 'CRM', 'Especialidade'])
    
    nova_tabela = pn.widgets.Tabulator(
        df, 
        selectable='checkbox', 
        disabled=True, 
        sizing_mode='stretch_width',
        widths={'ID': 50, 'Nome': 150, 'CRM': 100} 
    )
    
    container_tabela.objects = [nova_tabela]
    input_especs.options = [e.nome for e in session.query(Especialidade).all()]
    session.close()
    return nova_tabela

def salvar_medico(event):
    session = SessionLocal()
    try:
        nomes = input_especs.value
        especs_objs = session.query(Especialidade).filter(Especialidade.nome.in_(nomes)).all()
        
        if input_id.value:
            medico = session.query(Medico).filter(Medico.id == int(input_id.value)).first()
            medico.nome_completo = input_nome.value
            medico.crm = input_crm.value
            medico.especialidades[:] = especs_objs 
        else:
            novo = Medico(nome_completo=input_nome.value, crm=input_crm.value, especialidades=especs_objs)
            session.add(novo)
            
        session.commit()
        pn.state.notifications.success("Salvo com sucesso!")
        
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f"Erro ao salvar: verifique se o CRM já está em uso.")
    finally:
        session.close()
    
    input_id.value = ""
    input_nome.value = ""
    input_crm.value = ""
    input_especs.value = []
    
    carregar_dados()

def editar_medico(event):
    tab = container_tabela.objects[0]
    if not tab.selection: return
    row = tab.value.iloc[tab.selection[0]]
    input_id.value = str(row['ID'])
    input_nome.value = row['Nome']
    input_crm.value = row['CRM']
    input_especs.value = row['Especialidade'].split(', ') if row['Especialidade'] else []

def deletar_medico(event):
    tab = container_tabela.objects[0]
    
    if not tab.selection: 
        return
    
    ids_para_deletar = [int(tab.value.iloc[idx]['ID']) for idx in tab.selection]
    
    session = SessionLocal()
    try:
        for id_medico in ids_para_deletar:
            medico = session.query(Medico).filter(Medico.id == id_medico).first()
            if medico:
                session.delete(medico)
        
        session.commit()
        pn.state.notifications.success(f"{len(ids_para_deletar)} médico(s) removido(s) com sucesso!")
    except Exception as e:
        session.rollback()
        pn.state.notifications.error("Erro ao remover os registros.")
    finally:
        session.close()
        
    carregar_dados()

btn_salvar.on_click(salvar_medico)
btn_deletar.on_click(deletar_medico)
btn_editar.on_click(editar_medico)

carregar_dados()

template = pn.template.FastListTemplate(
    title="🏥 Sistema de Gestão Hospitalar",
    sidebar=["## Cadastro", input_id, input_nome, input_crm, input_especs, btn_salvar],
    main=[pn.Card(container_tabela, title="Médicos Cadastrados", sizing_mode='stretch_width'), pn.Row(btn_editar, btn_deletar)],
    accent_base_color="#1f77b4",
    header_background="#1f77b4",
    theme_toggle=False
)
template.servable()