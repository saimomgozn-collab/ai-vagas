import sqlite3
from datetime import datetime
from loguru import logger
import config
from scraper import init_db

def seed_database():
    """Popula a base de dados com vagas simuladas realistas em português para testes."""
    init_db()
    
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    vagas = [
        {
            "id": "mock_001",
            "title": "Engenheiro de Machine Learning",
            "company": "AeroTech IA",
            "location": "São Paulo, SP (Híbrido)",
            "description": (
                "Estamos buscando um Engenheiro de Machine Learning para liderar o desenvolvimento "
                "de modelos preditivos. Requisitos: Forte domínio em Python, bibliotecas como Pandas, "
                "Scikit-learn, TensorFlow ou PyTorch. Experiência com Docker, controle de versão Git, "
                "e APIs (FastAPI/Flask). Diferencial: experiência com pipelines MLOps e nuvem AWS."
            ),
            "url": "https://www.linkedin.com/jobs/view/mock_001",
            "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "keywords": "Machine Learning"
        },
        {
            "id": "mock_002",
            "title": "Cientista de Dados Pleno",
            "company": "Fintech Giga",
            "location": "Rio de Janeiro, RJ (Remoto)",
            "description": (
                "Vaga para Cientista de Dados focado em modelagem de risco e análise preditiva. "
                "Requisitos fundamentais: Fluência em Python (Pandas, Numpy), SQL avançado para "
                "extração de bases, modelagem estatística, testes A/B, e ferramentas de visualização "
                "como Power BI ou Tableau. Habilidade para traduzir dados em insights de negócios."
            ),
            "url": "https://www.linkedin.com/jobs/view/mock_002",
            "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "keywords": "Cientista de Dados"
        },
        {
            "id": "mock_003",
            "title": "Desenvolvedor Python Sênior",
            "company": "WebSoft Brasil",
            "location": "Belo Horizonte, MG (Híbrido)",
            "description": (
                "Buscamos engenheiro de software com forte experiência em desenvolvimento back-end "
                "com Python. Requisitos: Frameworks Django ou FastAPI, arquitetura MVC/Microserviços, "
                "bancos de dados PostgreSQL e Redis, e testes unitários. Conhecimento em pipelines CI/CD "
                "e Docker são essenciais. Conhecimento básico em análise de dados é bem-vindo."
            ),
            "url": "https://www.linkedin.com/jobs/view/mock_003",
            "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "keywords": "Desenvolvedor Python"
        },
        {
            "id": "mock_004",
            "title": "Desenvolvedor Front-end React / TypeScript",
            "company": "PixStudio",
            "location": "Remoto",
            "description": (
                "Procuramos profissional focado em Front-end para criar interfaces incríveis e dinâmicas. "
                "Requisitos obrigatórios: JavaScript ES6+, TypeScript, React (Hooks, Context API), HTML5, "
                "CSS3/Sass ou Tailwind CSS, e integração de APIs REST. Experiência com Figma "
                "e metodologias ágeis (Scrum)."
            ),
            "url": "https://www.linkedin.com/jobs/view/mock_004",
            "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "keywords": "Frontend"
        },
        {
            "id": "mock_005",
            "title": "Analista de Marketing Digital e SEO",
            "company": "Growth Hub",
            "location": "Curitiba, PR (Presencial)",
            "description": (
                "Vaga para Analista de Growth e Marketing Digital. Foco na criação de campanhas paga "
                "(Google Ads, Facebook Ads), SEO técnico para indexação, e redação de artigos/blogs. "
                "Requisitos: Google Analytics, SEMRush, excelente escrita, e facilidade para interpretar "
                "métricas de conversão. Não é necessário saber programar, mas afinidade com tecnologia ajuda."
            ),
            "url": "https://www.linkedin.com/jobs/view/mock_005",
            "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "keywords": "Marketing"
        }
    ]
    
    for vaga in vagas:
        cursor.execute("""
            INSERT OR REPLACE INTO jobs (id, title, company, location, description, url, date_scraped, keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            vaga['id'],
            vaga['title'],
            vaga['company'],
            vaga['location'],
            vaga['description'],
            vaga['url'],
            vaga['date_scraped'],
            vaga['keywords']
        ))
        
    conn.commit()
    conn.close()
    logger.info("Banco de dados populado com 5 vagas simuladas com sucesso!")

if __name__ == "__main__":
    seed_database()
