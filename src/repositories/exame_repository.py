import pandas as pd
from sqlalchemy import text
from src.database import get_engine

def listar_exames() -> pd.DataFrame:
    engine = get_engine()
    query = """
        SELECT 
            e.id_exame, 
            e.data_realizacao, 
            e.laudo, 
            p.nome_completo AS paciente, 
            t.nome_tipo AS tipo_exame, 
            i.nome_fantasia AS instituicao
        FROM exame e
        JOIN paciente p ON e.id_paciente = p.id_paciente
        JOIN tipo_exame t ON e.id_tipo = t.id_tipo
        JOIN instituicao_saude i ON e.id_instituicao = i.id_instituicao
        ORDER BY e.data_realizacao DESC;
    """
    return pd.read_sql_query(query, engine)

def obter_opcoes_pacientes() -> dict:
    engine = get_engine()
    df = pd.read_sql_query("SELECT id_paciente, nome_completo FROM paciente ORDER BY nome_completo;", engine)
    return {row['nome_completo']: row['id_paciente'] for _, row in df.iterrows()}

def obter_opcoes_tipos() -> dict:
    engine = get_engine()
    df = pd.read_sql_query("SELECT id_tipo, nome_tipo FROM tipo_exame ORDER BY nome_tipo;", engine)
    return {row['nome_tipo']: row['id_tipo'] for _, row in df.iterrows()}

def obter_opcoes_instituicoes() -> dict:
    engine = get_engine()
    df = pd.read_sql_query("SELECT id_instituicao, nome_fantasia FROM instituicao_saude ORDER BY nome_fantasia;", engine)
    return {row['nome_fantasia']: row['id_instituicao'] for _, row in df.iterrows()}

def cadastrar_exame(data_realizacao, laudo, id_paciente, id_tipo, id_instituicao) -> None:
    engine = get_engine()
    query = text("""
        INSERT INTO exame (data_realizacao, laudo, id_paciente, id_tipo, id_instituicao)
        VALUES (:data_realizacao, :laudo, :id_paciente, :id_tipo, :id_instituicao);
    """)
    with engine.begin() as connection:
        connection.execute(query, {
            "data_realizacao": data_realizacao, "laudo": laudo, 
            "id_paciente": id_paciente, "id_tipo": id_tipo, "id_instituicao": id_instituicao
        })

def atualizar_exame(id_exame, data_realizacao, laudo, id_paciente, id_tipo, id_instituicao) -> None:
    engine = get_engine()
    query = text("""
        UPDATE exame
        SET data_realizacao = :data_realizacao, laudo = :laudo, 
            id_paciente = :id_paciente, id_tipo = :id_tipo, id_instituicao = :id_instituicao
        WHERE id_exame = :id_exame;
    """)
    with engine.begin() as connection:
        connection.execute(query, {
            "id_exame": id_exame, "data_realizacao": data_realizacao, "laudo": laudo,
            "id_paciente": id_paciente, "id_tipo": id_tipo, "id_instituicao": id_instituicao
        })

def excluir_exame(id_exame) -> None:
    engine = get_engine()
    query = text("DELETE FROM exame WHERE id_exame = :id_exame;")
    with engine.begin() as connection:
        connection.execute(query, {"id_exame": id_exame})