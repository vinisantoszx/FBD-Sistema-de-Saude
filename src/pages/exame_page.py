import panel as pn
import pandas as pd
from src.repositories.exame_repository import (
    listar_exames, cadastrar_exame, atualizar_exame, excluir_exame,
    obter_opcoes_pacientes, obter_opcoes_tipos, obter_opcoes_instituicoes
)

def criar_pagina_exame():
    exame_selecionado = {"id_exame": None}

    data_input = pn.widgets.DatePicker(name="Data de Realização")
    laudo_input = pn.widgets.TextAreaInput(name="Laudo", placeholder="Digite o laudo do exame...", height=100)
    
    paciente_input = pn.widgets.Select(name="Paciente", options={})
    tipo_input = pn.widgets.Select(name="Tipo de Exame", options={})
    instituicao_input = pn.widgets.Select(name="Instituição", options={})

    mensagem = pn.pane.Alert("Preencha os dados para cadastrar um exame.", alert_type="info")
    tabela = pn.widgets.Tabulator(pd.DataFrame(), selectable=1, show_index=False, pagination="local", page_size=10, height=330)

    def carregar_dropdowns():
        try:
            paciente_input.options = obter_opcoes_pacientes()
            tipo_input.options = obter_opcoes_tipos()
            instituicao_input.options = obter_opcoes_instituicoes()
        except Exception:
            pass

    def carregar_tabela():
        try:
            tabela.value = listar_exames()
        except Exception as erro:
            tabela.value = pd.DataFrame()
            mensagem.object = f"Erro ao carregar exames: {erro}"
            mensagem.alert_type = "danger"

    def limpar_formulario():
        exame_selecionado["id_exame"] = None
        data_input.value = None
        laudo_input.value = ""
        tabela.selection = []
        mensagem.object = "Formulário limpo."
        mensagem.alert_type = "info"

    def cadastrar(event=None):
        if not data_input.value or not paciente_input.value:
            mensagem.object = "Preencha a data e selecione o paciente."
            mensagem.alert_type = "warning"
            return
        try:
            if exame_selecionado["id_exame"] is None:
                cadastrar_exame(data_input.value, laudo_input.value, paciente_input.value, tipo_input.value, instituicao_input.value)
                mensagem.object = "Exame cadastrado com sucesso."
            else:
                atualizar_exame(exame_selecionado["id_exame"], data_input.value, laudo_input.value, paciente_input.value, tipo_input.value, instituicao_input.value)
                mensagem.object = "Exame atualizado com sucesso."
            
            mensagem.alert_type = "success"
            carregar_tabela()
            limpar_formulario()
        except Exception as erro:
            mensagem.object = f"Erro: {erro}"
            mensagem.alert_type = "danger"

    def carregar_para_edicao(event=None):
        if not tabela.selection:
            mensagem.object = "Selecione um exame na tabela para editar."
            mensagem.alert_type = "warning"
            return
        
        indice = tabela.selection[0]
        linha = tabela.value.iloc[indice]
        
        exame_selecionado["id_exame"] = int(linha["id_exame"])
        
        if isinstance(linha["data_realizacao"], pd.Timestamp):
            data_input.value = linha["data_realizacao"].date()
        else:
            data_input.value = pd.to_datetime(linha["data_realizacao"]).date()
            
        laudo_input.value = linha["laudo"]
        
        paciente_input.value = obter_opcoes_pacientes().get(linha["paciente"])
        tipo_input.value = obter_opcoes_tipos().get(linha["tipo_exame"])
        instituicao_input.value = obter_opcoes_instituicoes().get(linha["instituicao"])
        
        mensagem.object = "Exame carregado. Altere o que desejar e clique em Salvar."
        mensagem.alert_type = "info"

    def excluir(event=None):
        if not tabela.selection:
            mensagem.object = "Selecione um exame na tabela para excluir."
            mensagem.alert_type = "warning"
            return
        indice = tabela.selection[0]
        id_exame = int(tabela.value.iloc[indice]["id_exame"])
        try:
            excluir_exame(id_exame)
            carregar_tabela()
            limpar_formulario()
            mensagem.object = "Exame excluído com sucesso."
            mensagem.alert_type = "success"
        except Exception as erro:
            mensagem.object = f"Erro ao excluir: {erro}"
            mensagem.alert_type = "danger"

    botao_salvar = pn.widgets.Button(name="Salvar (Cadastrar/Atualizar)", button_type="primary")
    botao_editar = pn.widgets.Button(name="Carregar Selecionado", button_type="warning")
    botao_excluir = pn.widgets.Button(name="Excluir", button_type="danger")
    botao_limpar = pn.widgets.Button(name="Limpar", button_type="light")

    botao_salvar.on_click(cadastrar)
    botao_editar.on_click(carregar_para_edicao)
    botao_excluir.on_click(excluir)
    botao_limpar.on_click(lambda event: limpar_formulario())

    formulario = pn.Card(
        pn.Column(
            pn.Row(data_input, paciente_input),
            pn.Row(tipo_input, instituicao_input),
            laudo_input,
            pn.Row(botao_salvar, botao_editar, botao_excluir, botao_limpar),
            mensagem,
        ), title="Formulário de Exame", collapsed=False
    )

    pagina = pn.Column(
        pn.pane.Markdown("# CRUD de Exames"),
        pn.pane.Markdown("Tela para inclusão, edição, remoção e listagem de exames."),
        formulario,
        pn.Card(tabela, title="Exames cadastrados", collapsed=False)
    )

    carregar_dropdowns()
    carregar_tabela()
    return pagina