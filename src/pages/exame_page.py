import panel as pn
import pandas as pd

from src.repositories.exame_repository import (
    listar_exames,
    cadastrar_exame,
    atualizar_exame,
    excluir_exame,
    obter_opcoes_pacientes,
    obter_opcoes_tipos,
    obter_opcoes_instituicoes,
)


def criar_pagina_exame():
    exame_selecionado = {"id_exame": None}

    id_input = pn.widgets.IntInput(
        name="ID do exame",
        start=1,
        value=0,
        placeholder="Digite o ID para editar ou excluir",
    )

    data_input = pn.widgets.DatePicker(
        name="Data de Realização",
    )

    laudo_input = pn.widgets.TextAreaInput(
        name="Laudo",
        placeholder="Digite o laudo do exame...",
        height=100,
    )

    paciente_input = pn.widgets.Select(
        name="Paciente",
        options={},
    )

    tipo_input = pn.widgets.Select(
        name="Tipo de Exame",
        options={},
    )

    instituicao_input = pn.widgets.Select(
        name="Instituição",
        options={},
    )

    mensagem = pn.pane.Alert(
        "Preencha os dados para cadastrar um exame.",
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

    def carregar_dropdowns():
        try:
            paciente_input.options = obter_opcoes_pacientes()
            tipo_input.options = obter_opcoes_tipos()
            instituicao_input.options = obter_opcoes_instituicoes()
        except Exception as erro:
            mensagem.object = f"Erro ao carregar opções: {erro}"
            mensagem.alert_type = "danger"

    def carregar_tabela():
        try:
            tabela.value = listar_exames()
        except Exception as erro:
            tabela.value = pd.DataFrame()
            mensagem.object = f"Erro ao carregar exames: {erro}"
            mensagem.alert_type = "danger"

    def limpar_formulario():
        exame_selecionado["id_exame"] = None

        id_input.value = 0
        data_input.value = None
        laudo_input.value = ""

        paciente_input.value = None
        tipo_input.value = None
        instituicao_input.value = None

        mensagem.object = "Formulário limpo."
        mensagem.alert_type = "info"

    def validar_formulario():
        campos_obrigatorios = [
            data_input.value,
            paciente_input.value,
            tipo_input.value,
            instituicao_input.value,
        ]

        return all(campos_obrigatorios)

    def salvar(event=None):
        if not validar_formulario():
            mensagem.object = "Preencha data, paciente, tipo de exame e instituição."
            mensagem.alert_type = "warning"
            return

        try:
            if exame_selecionado["id_exame"] is None:
                cadastrar_exame(
                    data_realizacao=data_input.value,
                    laudo=laudo_input.value,
                    id_paciente=paciente_input.value,
                    id_tipo=tipo_input.value,
                    id_instituicao=instituicao_input.value,
                )

                mensagem.object = "Exame cadastrado com sucesso."

            else:
                atualizar_exame(
                    id_exame=exame_selecionado["id_exame"],
                    data_realizacao=data_input.value,
                    laudo=laudo_input.value,
                    id_paciente=paciente_input.value,
                    id_tipo=tipo_input.value,
                    id_instituicao=instituicao_input.value,
                )

                mensagem.object = "Exame atualizado com sucesso."

            mensagem.alert_type = "success"

            carregar_tabela()
            limpar_formulario()

        except Exception as erro:
            mensagem.object = f"Erro ao salvar exame: {erro}"
            mensagem.alert_type = "danger"

    def carregar_para_edicao(event=None):
        id_exame = id_input.value

        if not id_exame or id_exame <= 0:
            mensagem.object = "Digite um ID válido para carregar o exame."
            mensagem.alert_type = "warning"
            return

        df = tabela.value

        if df.empty:
            mensagem.object = "A lista de exames está vazia."
            mensagem.alert_type = "warning"
            return

        resultado = df[df["id_exame"] == id_exame]

        if resultado.empty:
            mensagem.object = f"Nenhum exame encontrado com ID {id_exame}."
            mensagem.alert_type = "warning"
            return

        linha = resultado.iloc[0]

        exame_selecionado["id_exame"] = int(linha["id_exame"])

        if isinstance(linha["data_realizacao"], pd.Timestamp):
            data_input.value = linha["data_realizacao"].date()
        else:
            data_input.value = pd.to_datetime(linha["data_realizacao"]).date()

        laudo_input.value = linha["laudo"]

        paciente_input.value = obter_opcoes_pacientes().get(linha["paciente"])
        tipo_input.value = obter_opcoes_tipos().get(linha["tipo_exame"])
        instituicao_input.value = obter_opcoes_instituicoes().get(linha["instituicao"])

        mensagem.object = f"Exame ID {id_exame} carregado para edição."
        mensagem.alert_type = "info"

    def excluir(event=None):
        id_exame = id_input.value

        if not id_exame or id_exame <= 0:
            mensagem.object = "Digite um ID válido para excluir o exame."
            mensagem.alert_type = "warning"
            return

        try:
            excluir_exame(id_exame)

            carregar_tabela()
            limpar_formulario()

            mensagem.object = f"Exame ID {id_exame} excluído com sucesso."
            mensagem.alert_type = "success"

        except Exception as erro:
            mensagem.object = f"Erro ao excluir exame: {erro}"
            mensagem.alert_type = "danger"

    botao_salvar = pn.widgets.Button(
        name="Salvar cadastro/edição",
        button_type="primary",
    )

    botao_carregar = pn.widgets.Button(
        name="Carregar por ID",
        button_type="default",
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

    botao_salvar.on_click(salvar)
    botao_carregar.on_click(carregar_para_edicao)
    botao_excluir.on_click(excluir)
    botao_limpar.on_click(lambda event: limpar_formulario())
    botao_atualizar.on_click(lambda event: carregar_tabela())

    formulario = pn.Card(
        pn.Column(
            id_input,
            pn.Row(
                data_input,
                paciente_input,
            ),
            pn.Row(
                tipo_input,
                instituicao_input,
            ),
            laudo_input,
            pn.Row(
                botao_salvar,
                botao_carregar,
                botao_excluir,
                botao_limpar,
                botao_atualizar,
            ),
            mensagem,
        ),
        title="Formulário de Exame",
        collapsed=False,
    )

    pagina = pn.Column(
        pn.pane.Markdown("# CRUD de Exames"),
        pn.pane.Markdown(
            "Tela para inclusão, edição, remoção e listagem de exames cadastrados no banco de dados."
        ),
        formulario,
        pn.Card(
            tabela,
            title="Exames cadastrados",
            collapsed=False,
        ),
    )

    carregar_dropdowns()
    carregar_tabela()

    return pagina