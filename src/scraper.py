import re
import time
import sqlite3
import argparse
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from loguru import logger

# Importa configurações locais
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
            keywords TEXT
        )
    """)
    conn.commit()
    conn.close()
    logger.info("Banco de dados SQLite inicializado.")

def save_job(job_data):
    """Salva uma vaga no banco de dados SQLite, ignorando duplicatas pelo ID."""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO jobs (id, title, company, location, description, url, date_scraped, keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job_data['id'],
            job_data['title'],
            job_data['company'],
            job_data['location'],
            job_data['description'],
            job_data['url'],
            job_data['date_scraped'],
            job_data['keywords']
        ))
        conn.commit()
        logger.info(f"Vaga salva/atualizada: {job_data['title']} - {job_data['company']}")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar vaga no banco: {e}")
        return False
    finally:
        conn.close()

def is_job_scraped(job_id):
    """Verifica se a vaga já existe no banco de dados com descrição preenchida."""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jobs WHERE id = ? AND description IS NOT NULL AND description != ''", (job_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def clean_description(html_content):
    """Limpa o HTML da descrição da vaga para extrair o texto puro formatado."""
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    # Remove scripts e estilos
    for element in soup(["script", "style"]):
        element.decompose()
    
    # Substitui quebras de linha de bloco
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for p in soup.find_all(["p", "li", "div"]):
        p.append("\n")
        
    return soup.get_text()

def scrape_jobs(keywords, location=None, max_jobs=None):
    """Executa a raspagem de vagas no LinkedIn usando Playwright."""
    if location is None:
        location = config.LINKEDIN_LOCATION
    if max_jobs is None:
        max_jobs = config.MAX_JOBS_TO_SCRAPE
        
    init_db()
    
    logger.info(f"Iniciando scraping do LinkedIn. Termo: '{keywords}', Local: '{location}', Máx. Vagas: {max_jobs}")
    
    jobs_scraped_count = 0
    
    with sync_playwright() as p:
        # Usa um navegador Chromium realista com argumentos para diminuir detecção
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        # Configura um contexto de navegação com tamanho de tela realista e user-agent moderno
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        # Adiciona cookie de sessão se disponível
        if config.LINKEDIN_LI_AT:
            context.add_cookies([{
                'name': 'li_at',
                'value': config.LINKEDIN_LI_AT,
                'domain': '.www.linkedin.com',
                'path': '/'
            }])
            logger.info("Sessão autenticada do LinkedIn ativada via cookie li_at.")
        
        page = context.new_page()
        
        # Constrói URL de busca de vagas pública (guest)
        search_url = f"https://www.linkedin.com/jobs/search?keywords={keywords}&location={location}"
        logger.info(f"Navegando para: {search_url}")
        
        try:
            page.goto(search_url, wait_until="load", timeout=60000)
            time.sleep(3) # Aguarda renderização inicial
            
            # Verifica se fomos bloqueados ou redirecionados para login
            if "login" in page.url or "authwall" in page.url:
                logger.warning("Fomos redirecionados para a tela de login. Tentando contornar...")
            
            # Rola a página para carregar mais vagas
            logger.info("Rolando a página para carregar vagas...")
            for i in range(5):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(config.DELAY_BETWEEN_REQUESTS_SEC)
                
                # Tenta clicar no botão "Ver mais vagas" se aparecer
                see_more_button = page.locator("button.infinite-scroller__show-more-button")
                if see_more_button.is_visible():
                    try:
                        see_more_button.click()
                        logger.info("Botão 'Ver mais vagas' clicado.")
                        time.sleep(2)
                    except Exception:
                        pass
            
            # Coleta os links e IDs das vagas
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            
            # Encontra todos os cards de vagas
            job_cards = soup.find_all("div", class_=re.compile("base-card"))
            if not job_cards:
                job_cards = soup.find_all("li") # Fallback para itens da lista
                
            job_ids = []
            for card in job_cards:
                # Tenta extrair ID do atributo data-entity-urn ou data-id
                entity_urn = card.get("data-entity-urn")
                card_id = card.get("data-id")
                
                job_id = None
                if entity_urn and "jobPosting" in entity_urn:
                    job_id = entity_urn.split(":")[-1]
                elif card_id:
                    job_id = card_id
                else:
                    # Tenta extrair do link da vaga
                    link = card.find("a", class_=re.compile("base-card__full-link|job-search-card__image-link"))
                    if link and link.get("href"):
                        href = link.get("href")
                        match = re.search(r"/view/(\d+)", href)
                        if match:
                            job_id = match.group(1)
                
                if job_id and job_id not in job_ids:
                    job_ids.append(job_id)
            
            logger.info(f"Encontradas {len(job_ids)} vagas na página de busca.")
            
            # Itera em cada ID de vaga para coletar detalhes
            for idx, job_id in enumerate(job_ids):
                if jobs_scraped_count >= max_jobs:
                    logger.info("Limite de vagas alcançado.")
                    break
                    
                # Se já estiver raspada, pula
                if is_job_scraped(job_id):
                    logger.info(f"Vaga {job_id} já existe no banco. Pulando.")
                    jobs_scraped_count += 1
                    continue
                
                # Acessa a página de detalhes da vaga específica
                job_url = f"https://www.linkedin.com/jobs/view/{job_id}"
                logger.info(f"Coletando detalhes da vaga [{idx+1}/{len(job_ids)}]: {job_url}")
                
                try:
                    page.goto(job_url, wait_until="load", timeout=30000)
                    time.sleep(config.DELAY_BETWEEN_REQUESTS_SEC)
                    
                    detail_html = page.content()
                    detail_soup = BeautifulSoup(detail_html, "html.parser")
                    
                    # Extrai dados da vaga
                    # Classes comuns no layout público do LinkedIn
                    title_elem = detail_soup.find("h1", class_=re.compile("top-card-layout__title|topcard__title|job-details-jobs-unified-top-card__job-title"))
                    company_elem = detail_soup.find("a", class_=re.compile("topcard__org-name-link|topcard__org-name"))
                    if not company_elem:
                        company_elem = detail_soup.find("span", class_=re.compile("topcard__org-name"))
                        
                    location_elem = detail_soup.find("span", class_=re.compile("topcard__flavor--bullet|topcard__flavor"))
                    desc_elem = detail_soup.find("div", class_=re.compile("description__text|show-more-less-html__markup|jobs-description__content"))
                    
                    # Fallback para seletores caso o layout mude
                    title = title_elem.get_text(strip=True) if title_elem else "Título não disponível"
                    company = company_elem.get_text(strip=True) if company_elem else "Empresa não disponível"
                    location = location_elem.get_text(strip=True) if location_elem else "Local não disponível"
                    
                    description = clean_description(desc_elem) if desc_elem else ""
                    
                    # Se não conseguimos a descrição, tentamos seletores secundários
                    if not description:
                        # Às vezes o texto está num artigo ou sessão
                        sec_desc = detail_soup.find("section", class_=re.compile("description"))
                        if sec_desc:
                            description = clean_description(sec_desc)
                            
                    if not description:
                        logger.warning(f"Não foi possível extrair a descrição da vaga {job_id}. Pulando.")
                        continue
                        
                    job_data = {
                        "id": job_id,
                        "title": title,
                        "company": company,
                        "location": location,
                        "description": description,
                        "url": job_url,
                        "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "keywords": keywords
                    }
                    
                    if save_job(job_data):
                        jobs_scraped_count += 1
                        
                except Exception as e:
                    logger.error(f"Erro ao extrair detalhes da vaga {job_id}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Erro durante a navegação do scraper: {e}")
            
        finally:
            browser.close()
            
    logger.info(f"Scraping finalizado. {jobs_scraped_count} vagas prontas no banco de dados.")
    return jobs_scraped_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scraper de Vagas do LinkedIn")
    parser.add_argument("--keywords", type=str, default="Machine Learning", help="Palavra-chave para busca")
    parser.add_argument("--location", type=str, default="Brasil", help="Localidade")
    parser.add_argument("--limit", type=int, default=5, help="Limite de vagas a raspar")
    
    args = parser.parse_args()
    scrape_jobs(args.keywords, args.location, args.limit)
