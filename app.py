# MAIN DO PROJETO

import panel as pn

from src.pages.paciente_page import criar_pagina_paciente
from src.pages.medico_page import criar_pagina_medico

pn.extension("tabulator", notifications=True, sizing_mode="stretch_width")

abas = pn.Tabs(
    ("Pacientes", criar_pagina_paciente()),
    ("Médicos", criar_pagina_medico()),
)

layout = pn.template.FastListTemplate(
    title="Sistema de Monitoramento Colaborativo de Saúde",
    sidebar=[
        pn.pane.Markdown("## Menu"),
        pn.pane.Markdown("CRUD integrado ao PostgreSQL."),
        pn.pane.Markdown("Telas disponíveis: Pacientes e Médicos."),
    ],
    main=[
        abas,
    ],
)

layout.servable()