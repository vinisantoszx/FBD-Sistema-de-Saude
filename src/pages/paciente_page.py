import panel as pn
import pandas as pd

from src.repositories.paciente_repository import (
    listar_pacientes,
    cadastrar_paciente,
    atualizar_paciente,
    excluir_paciente,
)


def criar_pagina_paciente():
    paciente_selecionado = {"id_paciente": None}

    id_input = pn.widgets.IntInput(
        name="ID do paciente",
        start=1,
        value=0,
        placeholder="Digite o ID para editar ou excluir",
    )

    nome_input = pn.widgets.TextInput(
        name="Nome completo",
        placeholder="Ex.: Ana Clara Martins",
    )

    cpf_input = pn.widgets.TextInput(
        name="CPF",
        placeholder="000.000.000-00",
    )

    data_nascimento_input = pn.widgets.DatePicker(
        name="Data de nascimento",
    )

    email_input = pn.widgets.TextInput(
        name="E-mail",
        placeholder="paciente@email.com",
    )

    senha_input = pn.widgets.PasswordInput(
        name="Senha",
        placeholder="Digite a senha",
    )

    mensagem = pn.pane.Alert(
        "Preencha os dados para cadastrar um paciente.",
        alert_type="info",
    )

    tabela = pn.widgets.Tabulator(
        pd.DataFrame(),
        selectable=False,
        show_index=False,
        pagination="local",
        page_size=10,
        height=330,
    )

    def carregar_tabela():
        try:
            tabela.value = listar_pacientes()
        except Exception as erro:
            tabela.value = pd.DataFrame()
            mensagem.object = f"Erro ao carregar pacientes: {erro}"
            mensagem.alert_type = "danger"

    def limpar_formulario():
        paciente_selecionado["id_paciente"] = None

        id_input.value = 0
        nome_input.value = ""
        cpf_input.value = ""
        data_nascimento_input.value = None
        email_input.value = ""
        senha_input.value = ""

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

    def cadastrar(event=None):
        if not validar_formulario():
            mensagem.object = "Preencha todos os campos obrigatórios."
            mensagem.alert_type = "warning"
            return

        try:
            cadastrar_paciente(
                nome_completo=nome_input.value,
                cpf=cpf_input.value,
                data_nascimento=data_nascimento_input.value,
                email=email_input.value,
                senha=senha_input.value,
            )

            carregar_tabela()
            limpar_formulario()

            mensagem.object = "Paciente cadastrado com sucesso."
            mensagem.alert_type = "success"

        except Exception as erro:
            mensagem.object = f"Erro ao cadastrar paciente: {erro}"
            mensagem.alert_type = "danger"

    def carregar_para_edicao(event=None):
        id_paciente = id_input.value

        if not id_paciente or id_paciente <= 0:
            mensagem.object = "Digite um ID válido para carregar o paciente."
            mensagem.alert_type = "warning"
            return

        df = tabela.value

        if df.empty:
            mensagem.object = "A lista de pacientes está vazia."
            mensagem.alert_type = "warning"
            return

        resultado = df[df["id_paciente"] == id_paciente]

        if resultado.empty:
            mensagem.object = f"Nenhum paciente encontrado com ID {id_paciente}."
            mensagem.alert_type = "warning"
            return

        paciente = resultado.iloc[0]

        paciente_selecionado["id_paciente"] = int(paciente["id_paciente"])

        nome_input.value = paciente["nome_completo"]
        cpf_input.value = paciente["cpf"]

        if isinstance(paciente["data_nascimento"], pd.Timestamp):
            data_nascimento_input.value = paciente["data_nascimento"].date()
        else:
            data_nascimento_input.value = pd.to_datetime(
                paciente["data_nascimento"]
            ).date()

        email_input.value = paciente["email"]
        senha_input.value = paciente["senha"]

        mensagem.object = f"Paciente ID {id_paciente} carregado para edição."
        mensagem.alert_type = "info"

    def salvar_edicao(event=None):
        if paciente_selecionado["id_paciente"] is None:
            mensagem.object = "Carregue um paciente pelo ID antes de salvar a edição."
            mensagem.alert_type = "warning"
            return

        if not validar_formulario():
            mensagem.object = "Preencha todos os campos obrigatórios."
            mensagem.alert_type = "warning"
            return

        try:
            atualizar_paciente(
                id_paciente=paciente_selecionado["id_paciente"],
                nome_completo=nome_input.value,
                cpf=cpf_input.value,
                data_nascimento=data_nascimento_input.value,
                email=email_input.value,
                senha=senha_input.value,
            )

            carregar_tabela()
            limpar_formulario()

            mensagem.object = "Paciente atualizado com sucesso."
            mensagem.alert_type = "success"

        except Exception as erro:
            mensagem.object = f"Erro ao atualizar paciente: {erro}"
            mensagem.alert_type = "danger"

    def excluir(event=None):
        id_paciente = id_input.value

        if not id_paciente or id_paciente <= 0:
            mensagem.object = "Digite um ID válido para excluir o paciente."
            mensagem.alert_type = "warning"
            return

        try:
            excluir_paciente(id_paciente)

            carregar_tabela()
            limpar_formulario()

            mensagem.object = f"Paciente ID {id_paciente} excluído com sucesso."
            mensagem.alert_type = "success"

        except Exception as erro:
            mensagem.object = f"Erro ao excluir paciente: {erro}"
            mensagem.alert_type = "danger"

    botao_cadastrar = pn.widgets.Button(
        name="Cadastrar",
        button_type="primary",
    )

    botao_carregar = pn.widgets.Button(
        name="Carregar por ID",
        button_type="default",
    )

    botao_salvar = pn.widgets.Button(
        name="Salvar edição",
        button_type="success",
    )

    botao_excluir = pn.widgets.Button(
        name="Excluir por ID",
        button_type="danger",
    )

    botao_limpar = pn.widgets.Button(
        name="Limpar",
        button_type="light",
    )

    botao_atualizar = pn.widgets.Button(
        name="Atualizar lista",
        button_type="default",
    )

    botao_cadastrar.on_click(cadastrar)
    botao_carregar.on_click(carregar_para_edicao)
    botao_salvar.on_click(salvar_edicao)
    botao_excluir.on_click(excluir)
    botao_limpar.on_click(lambda event: limpar_formulario())
    botao_atualizar.on_click(lambda event: carregar_tabela())

    formulario = pn.Card(
        pn.Column(
            id_input,
            nome_input,
            cpf_input,
            data_nascimento_input,
            email_input,
            senha_input,
            pn.Row(
                botao_cadastrar,
                botao_carregar,
                botao_salvar,
                botao_excluir,
                botao_limpar,
                botao_atualizar,
            ),
            mensagem,
        ),
        title="Formulário de Paciente",
        collapsed=False,
    )

    pagina = pn.Column(
        pn.pane.Markdown("# CRUD de Pacientes"),
        pn.pane.Markdown(
            "Tela para inclusão, edição, remoção e listagem de pacientes cadastrados no banco de dados."
        ),
        formulario,
        pn.Card(
            tabela,
            title="Pacientes cadastrados",
            collapsed=False,
        ),
    )

    carregar_tabela()

    return pagina