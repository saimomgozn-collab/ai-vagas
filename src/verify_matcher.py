from loguru import logger
import config
from matcher import match_resume_with_database

def test_pipeline():
    logger.info("Iniciando teste de verificação do Matcher...")
    
    # Currículo de exemplo direcionado para Machine Learning / Data Science
    mock_resume = """
    Candidato de Tecnologia
    E-mail: candidato@email.com | Telefone: (11) 99999-9999
    
    Resumo Profissional:
    Profissional de tecnologia com 3 anos de experiência prática desenvolvendo modelos de inteligência artificial.
    Forte domínio em Python e análise de dados. Experiência sólida em pré-processamento de dados, engenharia de features
    e deploy de modelos preditivos em nuvem.
    
    Habilidades:
    - Linguagens: Python, SQL
    - Bibliotecas: Pandas, Numpy, Scikit-learn, TensorFlow
    - Ferramentas: Git, Docker, Flask
    """
    
    logger.info("Executando cruzamento semântico com a base de dados de vagas...")
    try:
        results = match_resume_with_database(mock_resume, limit=5)
        
        if not results:
            logger.error("Nenhum resultado retornado pelo matcher. O banco de dados de teste pode estar vazio.")
            return False
            
        logger.info(f"Retornadas {len(results)} recomendações de vagas. Resultados:")
        logger.info("-" * 60)
        
        for idx, match in enumerate(results):
            logger.info(f"Rank {idx+1}: {match['title']} - {match['company']}")
            logger.info(f"  Score de Aderência: {match['score_percentage']}%")
            logger.info(f"  Classificação: {match['fit_classification']}")
            logger.info(f"  Skills Presentes: {', '.join(match['skills_present'])}")
            logger.info(f"  Skills Faltantes: {', '.join(match['skills_missing'])}")
            logger.info(f"  Justificativa: {match['justification']}")
            logger.info("-" * 60)
            
        logger.info("Pipeline de Matching verificado com sucesso!")
        return True
    except Exception as e:
        logger.error(f"Erro durante a execução do teste de matching: {e}")
        return False

if __name__ == "__main__":
    test_pipeline()
