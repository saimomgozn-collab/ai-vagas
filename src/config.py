import os
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# Caminho raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega arquivo .env da raiz do projeto
load_dotenv(BASE_DIR / ".env")

# Cria diretórios necessários se não existirem
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Configurações do Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY não encontrada no arquivo .env. O sistema funcionará em modo local simplificado (TF-IDF).")

# Cookie de Sessão do LinkedIn (li_at)
LINKEDIN_LI_AT = os.getenv("LINKEDIN_LI_AT")
if LINKEDIN_LI_AT:
    logger.info("Token de sessão LINKEDIN_LI_AT carregado do .env.")


# Configurações do Scraper
LINKEDIN_LOCATION = os.getenv("LINKEDIN_LOCATION", "Brasil")
DEFAULT_KEYWORDS = [
    kw.strip() for kw in os.getenv("DEFAULT_KEYWORDS", "Machine Learning, Cientista de Dados, Desenvolvedor Python").split(",")
]
MAX_JOBS_TO_SCRAPE = int(os.getenv("MAX_JOBS_TO_SCRAPE", "30"))
DELAY_BETWEEN_REQUESTS_SEC = float(os.getenv("DELAY_BETWEEN_REQUESTS_SEC", "2.0"))

# Configurações do Banco de Dados
DATABASE_PATH = BASE_DIR / os.getenv("DATABASE_PATH", "data/vagas.db")

logger.info(f"Configurações carregadas com sucesso. BD: {DATABASE_PATH}")
