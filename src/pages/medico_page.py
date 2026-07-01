import panel as pn
import pandas as pd

from src.repositories.medico_repository import (
    listar_medicos,
    listar_especialidades,
    cadastrar_medico,
    atualizar_medico,
    excluir_medico,
)


def criar_pagina_medico():
    medico_selecionado = {"id_medico": None}

    id_input = pn.widgets.IntInput(
        name="ID do médico",
        start=1,
        value=0,
        placeholder="Digite o ID para editar ou excluir",
    )

    nome_input = pn.widgets.TextInput(
        name="Nome completo",
        placeholder="Ex.: Dra. Mariana Costa",
    )

    crm_input = pn.widgets.TextInput(
        name="CRM",
        placeholder="Ex.: CRM-CE 12345",
    )

    especialidades_input = pn.widgets.MultiChoice(
        name="Especialidades",
        options=[],
    )

    mensagem = pn.pane.Alert(
        "Preencha os dados para cadastrar um médico.",
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

    def carregar_especialidades():
        try:
            especialidades_input.options = listar_especialidades()
        except Exception as erro:
            especialidades_input.options = []
            mensagem.object = f"Erro ao carregar especialidades: {erro}"
            mensagem.alert_type = "danger"

    def carregar_tabela():
        try:
            tabela.value = listar_medicos()
        except Exception as erro:
            tabela.value = pd.DataFrame()
            mensagem.object = f"Erro ao carregar médicos: {erro}"
            mensagem.alert_type = "danger"

    def limpar_formulario():
        medico_selecionado["id_medico"] = None

        id_input.value = 0
        nome_input.value = ""
        crm_input.value = ""
        especialidades_input.value = []

        mensagem.object = "Formulário limpo."
        mensagem.alert_type = "info"

    def validar_formulario():
        campos_obrigatorios = [
            nome_input.value,
            crm_input.value,
            especialidades_input.value,
        ]

        return all(campos_obrigatorios)

    def cadastrar(event=None):
        if not validar_formulario():
            mensagem.object = "Preencha nome, CRM e ao menos uma especialidade."
            mensagem.alert_type = "warning"
            return

        try:
            cadastrar_medico(
                nome_completo=nome_input.value,
                crm=crm_input.value,
                especialidades=especialidades_input.value,
            )

            carregar_tabela()
            limpar_formulario()

            mensagem.object = "Médico cadastrado com sucesso."
            mensagem.alert_type = "success"

        except Exception as erro:
            mensagem.object = f"Erro ao cadastrar médico: {erro}"
            mensagem.alert_type = "danger"

    def carregar_para_edicao(event=None):
        id_medico = id_input.value

        if not id_medico or id_medico <= 0:
            mensagem.object = "Digite um ID válido para carregar o médico."
            mensagem.alert_type = "warning"
            return

        df = tabela.value

        if df.empty:
            mensagem.object = "A lista de médicos está vazia."
            mensagem.alert_type = "warning"
            return

        resultado = df[df["id_medico"] == id_medico]

        if resultado.empty:
            mensagem.object = f"Nenhum médico encontrado com ID {id_medico}."
            mensagem.alert_type = "warning"
            return

        medico = resultado.iloc[0]

        medico_selecionado["id_medico"] = int(medico["id_medico"])

        nome_input.value = medico["nome_completo"]
        crm_input.value = medico["crm"]

        if medico["especialidades"]:
            especialidades_input.value = medico["especialidades"].split(", ")
        else:
            especialidades_input.value = []

        mensagem.object = f"Médico ID {id_medico} carregado para edição."
        mensagem.alert_type = "info"

    def salvar_edicao(event=None):
        if medico_selecionado["id_medico"] is None:
            mensagem.object = "Carregue um médico pelo ID antes de salvar a edição."
            mensagem.alert_type = "warning"
            return

        if not validar_formulario():
            mensagem.object = "Preencha nome, CRM e ao menos uma especialidade."
            mensagem.alert_type = "warning"
            return

        try:
            atualizar_medico(
                id_medico=medico_selecionado["id_medico"],
                nome_completo=nome_input.value,
                crm=crm_input.value,
                especialidades=especialidades_input.value,
            )

            carregar_tabela()
            limpar_formulario()

            mensagem.object = "Médico atualizado com sucesso."
            mensagem.alert_type = "success"

        except Exception as erro:
            mensagem.object = f"Erro ao atualizar médico: {erro}"
            mensagem.alert_type = "danger"

    def excluir(event=None):
        id_medico = id_input.value

        if not id_medico or id_medico <= 0:
            mensagem.object = "Digite um ID válido para excluir o médico."
            mensagem.alert_type = "warning"
            return

        try:
            excluir_medico(id_medico)

            carregar_tabela()
            limpar_formulario()

            mensagem.object = f"Médico ID {id_medico} excluído com sucesso."
            mensagem.alert_type = "success"

        except Exception as erro:
            mensagem.object = f"Erro ao excluir médico: {erro}"
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
            crm_input,
            especialidades_input,
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
        title="Formulário de Médico",
        collapsed=False,
    )

    pagina = pn.Column(
        pn.pane.Markdown("# CRUD de Médicos"),
        pn.pane.Markdown(
            "Tela para inclusão, edição, remoção e listagem de médicos cadastrados no banco de dados."
        ),
        formulario,
        pn.Card(
            tabela,
            title="Médicos cadastrados",
            collapsed=False,
        ),
    )

    carregar_especialidades()
    carregar_tabela()

    return pagina