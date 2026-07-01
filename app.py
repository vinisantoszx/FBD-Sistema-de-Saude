# MAIN DO PROJETO

import panel as pn

from src.pages.paciente_page import criar_pagina_paciente
from src.pages.medico_page import criar_pagina_medico
from src.pages.exame_page import criar_pagina_exame

pn.extension("tabulator", notifications=True, sizing_mode="stretch_width")

abas = pn.Tabs(
    ("Pacientes", criar_pagina_paciente()),
    ("Médicos", criar_pagina_medico()),
    ("Exames", criar_pagina_exame()),
)

layout = pn.template.FastListTemplate(
    title="Sistema de Monitoramento Colaborativo de Saúde",
    sidebar=[
        pn.pane.Markdown("## Menu"),
        pn.pane.Markdown("CRUD integrado ao PostgreSQL."),
        pn.pane.Markdown("Telas disponíveis: Pacientes, Médicos e Exames."),
    ],
    main=[
        abas,
    ],
)

layout.servable()
