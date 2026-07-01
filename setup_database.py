from pathlib import Path

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, text

from src.database import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def criar_banco_se_nao_existir() -> None:
    print(f"Verificando se o banco '{DB_NAME}' existe...")

    conexao = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
    )

    conexao.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s;",
            (DB_NAME,),
        )

        banco_existe = cursor.fetchone()

        if banco_existe:
            print(f"Banco '{DB_NAME}' já existe.")
        else:
            cursor.execute(f'CREATE DATABASE "{DB_NAME}";')
            print(f"Banco '{DB_NAME}' criado com sucesso.")

        cursor.close()

    finally:
        conexao.close()


def obter_engine_banco():
    url = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return create_engine(url)


def executar_script_sql(caminho_arquivo: str) -> None:
    caminho = Path(caminho_arquivo)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    conteudo_sql = caminho.read_text(encoding="utf-8")

    comandos = [
        comando.strip()
        for comando in conteudo_sql.split(";")
        if comando.strip()
    ]

    engine = obter_engine_banco()

    with engine.begin() as connection:
        for comando in comandos:
            connection.execute(text(comando))


def configurar_banco() -> None:
    criar_banco_se_nao_existir()

    print("Criando tabelas...")
    executar_script_sql("database/create_tables.sql")

    print("Inserindo dados iniciais...")
    executar_script_sql("database/insert_data.sql")

    print("Banco configurado com sucesso!")


if __name__ == "__main__":
    try:
        configurar_banco()
    except Exception as erro:
        print("Erro ao configurar o banco de dados:")
        print(erro)