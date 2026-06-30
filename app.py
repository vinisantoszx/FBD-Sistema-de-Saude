import panel as pn

from src.pages.paciente_page import criar_pagina_paciente

pn.extension("tabulator", sizing_mode="stretch_width")

layout = pn.template.FastListTemplate(
    title="Sistema de Monitoramento Colaborativo de Saúde",
    sidebar=[
        pn.pane.Markdown("## Menu"),
        pn.pane.Markdown("**Tela atual:** Pacientes"),
        pn.pane.Markdown("CRUD integrado ao PostgreSQL."),
    ],
    main=[
        criar_pagina_paciente(),
    ],
)

layout.servable()