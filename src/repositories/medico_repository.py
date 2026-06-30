import pandas as pd
from sqlalchemy import text

from src.database import get_engine


def listar_medicos() -> pd.DataFrame:
    engine = get_engine()

    query = """
        SELECT
            m.id_medico,
            m.nome_completo,
            m.crm,
            COALESCE(
                STRING_AGG(e.nome_especialidade, ', ' ORDER BY e.nome_especialidade),
                ''
            ) AS especialidades
        FROM medico m
        LEFT JOIN medico_especialidade me
            ON m.id_medico = me.id_medico
        LEFT JOIN especialidade e
            ON me.id_especialidade = e.id_especialidade
        GROUP BY
            m.id_medico,
            m.nome_completo,
            m.crm
        ORDER BY m.id_medico;
    """

    return pd.read_sql_query(query, engine)


def listar_especialidades() -> list[str]:
    engine = get_engine()

    query = """
        SELECT nome_especialidade
        FROM especialidade
        ORDER BY nome_especialidade;
    """

    df = pd.read_sql_query(query, engine)

    return df["nome_especialidade"].tolist()


def cadastrar_medico(nome_completo, crm, especialidades) -> None:
    engine = get_engine()

    inserir_medico = text("""
        INSERT INTO medico (
            nome_completo,
            crm
        )
        VALUES (
            :nome_completo,
            :crm
        )
        RETURNING id_medico;
    """)

    buscar_especialidade = text("""
        SELECT id_especialidade
        FROM especialidade
        WHERE nome_especialidade = :nome_especialidade;
    """)

    inserir_relacao = text("""
        INSERT INTO medico_especialidade (
            id_medico,
            id_especialidade
        )
        VALUES (
            :id_medico,
            :id_especialidade
        );
    """)

    with engine.begin() as connection:
        resultado = connection.execute(
            inserir_medico,
            {
                "nome_completo": nome_completo,
                "crm": crm,
            },
        )

        id_medico = resultado.scalar_one()

        for nome_especialidade in especialidades:
            resultado_especialidade = connection.execute(
                buscar_especialidade,
                {
                    "nome_especialidade": nome_especialidade,
                },
            )

            id_especialidade = resultado_especialidade.scalar_one_or_none()

            if id_especialidade is not None:
                connection.execute(
                    inserir_relacao,
                    {
                        "id_medico": id_medico,
                        "id_especialidade": id_especialidade,
                    },
                )


def atualizar_medico(id_medico, nome_completo, crm, especialidades) -> None:
    engine = get_engine()

    atualizar = text("""
        UPDATE medico
        SET
            nome_completo = :nome_completo,
            crm = :crm
        WHERE id_medico = :id_medico;
    """)

    remover_relacoes = text("""
        DELETE FROM medico_especialidade
        WHERE id_medico = :id_medico;
    """)

    buscar_especialidade = text("""
        SELECT id_especialidade
        FROM especialidade
        WHERE nome_especialidade = :nome_especialidade;
    """)

    inserir_relacao = text("""
        INSERT INTO medico_especialidade (
            id_medico,
            id_especialidade
        )
        VALUES (
            :id_medico,
            :id_especialidade
        );
    """)

    with engine.begin() as connection:
        connection.execute(
            atualizar,
            {
                "id_medico": id_medico,
                "nome_completo": nome_completo,
                "crm": crm,
            },
        )

        connection.execute(
            remover_relacoes,
            {
                "id_medico": id_medico,
            },
        )

        for nome_especialidade in especialidades:
            resultado_especialidade = connection.execute(
                buscar_especialidade,
                {
                    "nome_especialidade": nome_especialidade,
                },
            )

            id_especialidade = resultado_especialidade.scalar_one_or_none()

            if id_especialidade is not None:
                connection.execute(
                    inserir_relacao,
                    {
                        "id_medico": id_medico,
                        "id_especialidade": id_especialidade,
                    },
                )


def excluir_medico(id_medico) -> None:
    engine = get_engine()

    remover_relacoes = text("""
        DELETE FROM medico_especialidade
        WHERE id_medico = :id_medico;
    """)

    remover_medico = text("""
        DELETE FROM medico
        WHERE id_medico = :id_medico;
    """)

    with engine.begin() as connection:
        connection.execute(
            remover_relacoes,
            {
                "id_medico": id_medico,
            },
        )

        connection.execute(
            remover_medico,
            {
                "id_medico": id_medico,
            },
        )