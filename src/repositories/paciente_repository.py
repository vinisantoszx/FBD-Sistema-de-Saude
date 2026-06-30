import pandas as pd
from sqlalchemy import text

from src.database import get_engine


def listar_pacientes() -> pd.DataFrame:
    engine = get_engine()

    query = """
        SELECT
            id_paciente,
            nome_completo,
            cpf,
            data_nascimento,
            email,
            senha
        FROM paciente
        ORDER BY id_paciente;
    """

    return pd.read_sql_query(query, engine)


def cadastrar_paciente(nome_completo, cpf, data_nascimento, email, senha) -> None:
    engine = get_engine()

    query = text("""
        INSERT INTO paciente (
            nome_completo,
            cpf,
            data_nascimento,
            email,
            senha
        )
        VALUES (
            :nome_completo,
            :cpf,
            :data_nascimento,
            :email,
            :senha
        );
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "nome_completo": nome_completo,
                "cpf": cpf,
                "data_nascimento": data_nascimento,
                "email": email,
                "senha": senha,
            },
        )


def atualizar_paciente(
    id_paciente,
    nome_completo,
    cpf,
    data_nascimento,
    email,
    senha,
) -> None:
    engine = get_engine()

    query = text("""
        UPDATE paciente
        SET
            nome_completo = :nome_completo,
            cpf = :cpf,
            data_nascimento = :data_nascimento,
            email = :email,
            senha = :senha
        WHERE id_paciente = :id_paciente;
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "id_paciente": id_paciente,
                "nome_completo": nome_completo,
                "cpf": cpf,
                "data_nascimento": data_nascimento,
                "email": email,
                "senha": senha,
            },
        )


def excluir_paciente(id_paciente) -> None:
    engine = get_engine()

    query = text("""
        DELETE FROM paciente
        WHERE id_paciente = :id_paciente;
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "id_paciente": id_paciente,
            },
        )