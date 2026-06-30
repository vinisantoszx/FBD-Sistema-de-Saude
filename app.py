import panel as pn
import pandas as pd

pn.extension("tabulator", sizing_mode="stretch_width")

pacientes = pd.DataFrame(
    columns=[
        "id_paciente",
        "nome_completo",
        "cpf",
        "data_nascimento",
        "email",
        "senha",
    ]
)

contador_id = 1
paciente_selecionado = None

nome_input = pn.widgets.TextInput(name="Nome completo", placeholder="Ex.: Ana Clara Martins")
cpf_input = pn.widgets.TextInput(name="CPF", placeholder="000.000.000-00")
data_nascimento_input = pn.widgets.DatePicker(name="Data de nascimento")
email_input = pn.widgets.TextInput(name="E-mail", placeholder="paciente@email.com")
senha_input = pn.widgets.PasswordInput(name="Senha", placeholder="Digite a senha")

mensagem = pn.pane.Alert("Preencha os dados para cadastrar um paciente.", alert_type="info")

tabela = pn.widgets.Tabulator(
    pacientes,
    selectable=1,
    show_index=False,
    pagination="local",
    page_size=10,
    height=330,
)


def limpar_formulario():
    global paciente_selecionado

    paciente_selecionado = None
    nome_input.value = ""
    cpf_input.value = ""
    data_nascimento_input.value = None
    email_input.value = ""
    senha_input.value = ""
    tabela.selection = []
    mensagem.object = "Formulário limpo."
    mensagem.alert_type = "info"


def validar_formulario():
    campos_obrigatorios = [
        nome_input.value,
        cpf_input.value,
        data_nascimento_input.value,
        email_input.value,
        senha_input.value,
    ]

    return all(campos_obrigatorios)


def atualizar_tabela():
    tabela.value = pacientes.copy()


def cadastrar_paciente(event=None):
    global pacientes, contador_id

    if not validar_formulario():
        mensagem.object = "Preencha todos os campos obrigatórios."
        mensagem.alert_type = "warning"
        return

    novo_paciente = {
        "id_paciente": contador_id,
        "nome_completo": nome_input.value,
        "cpf": cpf_input.value,
        "data_nascimento": data_nascimento_input.value,
        "email": email_input.value,
        "senha": senha_input.value,
    }

    pacientes = pd.concat([pacientes, pd.DataFrame([novo_paciente])], ignore_index=True)
    contador_id += 1
    atualizar_tabela()
    limpar_formulario()
    mensagem.object = "Paciente cadastrado com sucesso."
    mensagem.alert_type = "success"


def carregar_paciente(event=None):
    global paciente_selecionado

    if not tabela.selection:
        mensagem.object = "Selecione um paciente na tabela para editar."
        mensagem.alert_type = "warning"
        return

    indice = tabela.selection[0]
    paciente = pacientes.iloc[indice]
    paciente_selecionado = indice

    nome_input.value = paciente["nome_completo"]
    cpf_input.value = paciente["cpf"]
    data_nascimento_input.value = paciente["data_nascimento"]
    email_input.value = paciente["email"]
    senha_input.value = paciente["senha"]

    mensagem.object = "Paciente carregado para edição."
    mensagem.alert_type = "info"


def salvar_edicao(event=None):
    global pacientes, paciente_selecionado

    if paciente_selecionado is None:
        mensagem.object = "Carregue um paciente antes de salvar a edição."
        mensagem.alert_type = "warning"
        return

    if not validar_formulario():
        mensagem.object = "Preencha todos os campos obrigatórios."
        mensagem.alert_type = "warning"
        return

    pacientes.loc[paciente_selecionado, "nome_completo"] = nome_input.value
    pacientes.loc[paciente_selecionado, "cpf"] = cpf_input.value
    pacientes.loc[paciente_selecionado, "data_nascimento"] = data_nascimento_input.value
    pacientes.loc[paciente_selecionado, "email"] = email_input.value
    pacientes.loc[paciente_selecionado, "senha"] = senha_input.value

    atualizar_tabela()
    limpar_formulario()
    mensagem.object = "Paciente atualizado com sucesso."
    mensagem.alert_type = "success"


def excluir_paciente(event=None):
    global pacientes

    if not tabela.selection:
        mensagem.object = "Selecione um paciente na tabela para excluir."
        mensagem.alert_type = "warning"
        return

    indice = tabela.selection[0]
    pacientes = pacientes.drop(pacientes.index[indice]).reset_index(drop=True)
    atualizar_tabela()
    limpar_formulario()
    mensagem.object = "Paciente excluído com sucesso."
    mensagem.alert_type = "success"


botao_cadastrar = pn.widgets.Button(name="Cadastrar", button_type="primary")
botao_carregar = pn.widgets.Button(name="Carregar para edição", button_type="default")
botao_salvar = pn.widgets.Button(name="Salvar edição", button_type="success")
botao_excluir = pn.widgets.Button(name="Excluir", button_type="danger")
botao_limpar = pn.widgets.Button(name="Limpar", button_type="light")

botao_cadastrar.on_click(cadastrar_paciente)
botao_carregar.on_click(carregar_paciente)
botao_salvar.on_click(salvar_edicao)
botao_excluir.on_click(excluir_paciente)
botao_limpar.on_click(lambda event: limpar_formulario())

formulario = pn.Card(
    pn.Column(
        nome_input,
        cpf_input,
        data_nascimento_input,
        email_input,
        senha_input,
        pn.Row(botao_cadastrar, botao_carregar, botao_salvar, botao_excluir, botao_limpar),
        mensagem,
    ),
    title="Formulário de Paciente",
    collapsed=False,
)

layout = pn.template.FastListTemplate(
    title="Sistema de Monitoramento Colaborativo de Saúde",
    sidebar=[
        pn.pane.Markdown("## Menu"),
        pn.pane.Markdown("**Tela atual:** Pacientes"),
        pn.pane.Markdown("Interface inicial sem conexão com banco de dados."),
    ],
    main=[
        pn.pane.Markdown("# CRUD de Pacientes"),
        pn.pane.Markdown(
            "Tela inicial para inclusão, edição, remoção e listagem de pacientes."
        ),
        formulario,
        pn.Card(tabela, title="Pacientes cadastrados", collapsed=False),
    ],
)

layout.servable()
