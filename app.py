import panel as pn

from src.pages.paciente_page import criar_pagina_paciente
## from src.pages.medico_page import criar_pagina_medico
## from src.pages.consulta_page import criar_pagina_consulta

pn.extension("tabulator", sizing_mode="stretch_width")

abas = pn.Tabs(
    ("Pacientes", criar_pagina_paciente()),
    ## ("Médicos", criar_pagina_medico()),
    ## ("Consultas", criar_pagina_consulta()),
)

layout = pn.template.FastListTemplate(
    title="Sistema de Monitoramento Colaborativo de Saúde",
    sidebar=[
        pn.pane.Markdown("## Menu"),
        pn.pane.Markdown("Sistema de CRUD com PostgreSQL"),
    ],
    main=[
        abas
    ],
)

layout.servable()