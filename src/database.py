import sqlite3
import pandas as pd
from pathlib import Path
from loguru import logger
import config

def init_db():
    """Inicializa o banco de dados SQLite e cria a tabela de vagas se não existir."""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            description TEXT,
            url TEXT,
            date_scraped TEXT,
            work_type TEXT,
            experience_level TEXT
        )
    """)
    conn.commit()
    conn.close()
    logger.info("Banco de dados SQLite inicializado.")

def import_kaggle_csv(csv_path: str, chunk_size: int = 5000, max_rows: int = None) -> dict:
    """
    Importa o arquivo CSV do Kaggle de vagas do LinkedIn para o banco de dados SQLite em blocos.
    Oferece mapeamento inteligente de colunas com fallbacks.
    """
    init_db()
    
    csv_file = Path(csv_path)
    if not csv_file.exists():
        logger.error(f"Arquivo CSV não encontrado em: {csv_path}")
        return {"status": "error", "message": "Arquivo CSV não encontrado."}
        
    logger.info(f"Iniciando importação do CSV: {csv_path}")
    
    # Mapeamento inteligente de colunas do CSV para o nosso Banco
    possible_mappings = {
        'id': ['job_id', 'id', 'id_vaga'],
        'title': ['title', 'job_title', 'titulo', 'name'],
        'company': ['company_name', 'company', 'empresa'],
        'location': ['location', 'localizacao', 'city'],
        'description': ['description', 'job_description', 'descricao'],
        'url': ['job_link', 'url', 'link'],
        'work_type': ['work_type', 'formatted_work_type', 'tipo_trabalho'],
        'experience_level': ['experience_level', 'formatted_experience_level', 'nivel_experiencia']
    }
    
    conn = sqlite3.connect(config.DATABASE_PATH)
    total_imported = 0
    total_skipped = 0
    
    try:
        # Lê a primeira linha para identificar colunas e criar o mapa
        first_chunk = pd.read_csv(csv_path, nrows=2)
        columns = first_chunk.columns.tolist()
        
        active_mapping = {}
        for db_col, csv_cols in possible_mappings.items():
            for csv_col in csv_cols:
                if csv_col in columns:
                    active_mapping[csv_col] = db_col
                    break
        
        logger.info(f"Colunas do CSV mapeadas para importação: {active_mapping}")
        
        # Lê o CSV em lotes (chunks) para economizar memória (útil para 124 mil linhas)
        chunk_iter = pd.read_csv(csv_path, chunksize=chunk_size)
        
        for idx, chunk in enumerate(chunk_iter):
            if max_rows and total_imported >= max_rows:
                logger.info(f"Limite máximo de {max_rows} linhas importadas alcançado.")
                break
                
            # Renomeia as colunas conforme mapeamento ativo
            chunk_filtered = chunk.rename(columns=active_mapping)
            
            # Filtra apenas as colunas que pertencem à tabela
            db_cols = ['id', 'title', 'company', 'location', 'description', 'url', 'work_type', 'experience_level']
            # Mantém apenas as colunas que conseguimos mapear
            present_cols = [col for col in db_cols if col in chunk_filtered.columns]
            chunk_to_insert = chunk_filtered[present_cols].copy()
            
            # Garante que temos a coluna ID
            if 'id' not in chunk_to_insert.columns:
                # Se não houver ID no CSV, gera um ID baseado no índice
                chunk_to_insert['id'] = [f"kaggle_{total_imported + i}" for i in range(len(chunk_to_insert))]
            else:
                # Converte ID para string e limpa vazios
                chunk_to_insert['id'] = chunk_to_insert['id'].astype(str)
                chunk_to_insert = chunk_to_insert.dropna(subset=['id'])
                
            # Garante que temos a coluna URL
            if 'url' not in chunk_to_insert.columns:
                # Cria um link padrão com base no ID
                chunk_to_insert['url'] = "https://www.linkedin.com/jobs/view/" + chunk_to_insert['id']
                
            # Adiciona data de importação
            chunk_to_insert['date_scraped'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Limpa valores nulos do pandas para compatibilidade com SQLite
            chunk_to_insert = chunk_to_insert.fillna("")
            
            # Insere no SQLite substituindo se houver ID repetido
            cursor = conn.cursor()
            for _, row in chunk_to_insert.iterrows():
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO jobs (id, title, company, location, description, url, date_scraped, work_type, experience_level)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        str(row.get('id', '')),
                        str(row.get('title', '')),
                        str(row.get('company', '')),
                        str(row.get('location', '')),
                        str(row.get('description', '')),
                        str(row.get('url', '')),
                        str(row.get('date_scraped', '')),
                        str(row.get('work_type', '')),
                        str(row.get('experience_level', ''))
                    ))
                    total_imported += 1
                except Exception as e:
                    total_skipped += 1
                    
            conn.commit()
            logger.info(f"Lote {idx+1} processado. Vagas importadas até o momento: {total_imported}")
            
        return {
            "status": "success",
            "imported": total_imported,
            "skipped": total_skipped,
            "message": f"Sucesso! {total_imported} vagas importadas para o banco de dados."
        }
    except Exception as e:
        logger.error(f"Erro ao processar importação do CSV: {e}")
        return {"status": "error", "message": f"Erro de processamento: {str(e)}"}
    finally:
        conn.close()
