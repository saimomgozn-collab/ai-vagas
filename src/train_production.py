import os
import pickle
import random
import numpy as np
from loguru import logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def main():
    logger.info("Iniciando Pipeline Avançado de Machine Learning...")
    logger.info("Carregando dataset de Fit/No Fit e Salários...")

    resumes = []
    jobs = []
    labels = []
    salaries = []
    
    tech_stacks = [
        (["python", "pandas", "numpy", "machine learning", "sql"], ["data scientist", "analista de dados", "cientista de dados"], (10000, 18000)),
        (["java", "spring boot", "microserviços", "api", "backend"], ["desenvolvedor backend", "engenheiro java", "backend senior"], (8000, 15000)),
        (["react", "typescript", "javascript", "html", "css", "frontend"], ["desenvolvedor frontend", "frontend engineer", "react developer"], (6000, 12000)),
        (["aws", "docker", "kubernetes", "ci/cd", "terraform", "devops"], ["engenheiro devops", "cloud architect", "sre"], (12000, 20000)),
        (["c#", ".net", "sql server", "azure", "backend"], ["desenvolvedor .net", "engenheiro de software c#"], (8000, 15000))
    ]
    
    random.seed(42)
    
    for _ in range(500):
        stack_idx = random.randint(0, len(tech_stacks)-1)
        skills, titles, salary_range = tech_stacks[stack_idx]
        
        r_text = f"Experiência como {random.choice(titles)}. Habilidades: {', '.join(random.sample(skills, k=3))}."
        j_text = f"Vaga para {random.choice(titles)}. Requisitos: {', '.join(random.sample(skills, k=3))} e experiência."
        
        resumes.append(r_text)
        jobs.append(j_text)
        labels.append(1)
        salaries.append(random.uniform(salary_range[0], salary_range[1]))
        
        stack_idx_r = random.randint(0, len(tech_stacks)-1)
        stack_idx_j = random.choice([i for i in range(len(tech_stacks)) if i != stack_idx_r])
        
        skills_r, titles_r, _ = tech_stacks[stack_idx_r]
        skills_j, titles_j, salary_range_j = tech_stacks[stack_idx_j]
        
        r_text_nofit = f"Experiência como {random.choice(titles_r)}. Habilidades: {', '.join(random.sample(skills_r, k=3))}."
        j_text_nofit = f"Vaga para {random.choice(titles_j)}. Requisitos: {', '.join(random.sample(skills_j, k=3))} e experiência avançada."
        
        resumes.append(r_text_nofit)
        jobs.append(j_text_nofit)
        labels.append(0)
        salaries.append(random.uniform(salary_range_j[0], salary_range_j[1]))

    for i in range(50):
        labels[i] = 0 if labels[i] == 1 else 1
        
    logger.info("Aplicando NLP: TF-IDF com Bigramas...")
    vectorizer = TfidfVectorizer(max_features=1500, ngram_range=(1, 2))
    vectorizer.fit(resumes + jobs)
    
    v_resumes = vectorizer.transform(resumes)
    v_jobs = vectorizer.transform(jobs)
    
    X_class = abs(v_jobs - v_resumes)
    y_class = np.array(labels)

    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_class, y_class, test_size=0.2, random_state=42)

    logger.info("Treinando classificador...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
    clf.fit(X_train_c, y_train_c)
    y_pred_c = clf.predict(X_test_c)
    
    logger.info("Treinando regressor para salários...")
    X_reg = v_jobs
    y_reg = np.array(salaries)
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
    
    reg = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42)
    reg.fit(X_train_r, y_train_r)
    y_pred_r = reg.predict(X_test_r)

    print("\n" + "="*55)
    print(" 📊 RELATÓRIO OFICIAL")
    print("="*55)
    print("--- CLASSIFICAÇÃO (FIT / NO FIT) ---")
    print(classification_report(y_test_c, y_pred_c, target_names=["No Fit (0)", "Fit (1)"]))
    
    mae = mean_absolute_error(y_test_r, y_pred_r)
    rmse = np.sqrt(mean_squared_error(y_test_r, y_pred_r))
    r2 = r2_score(y_test_r, y_pred_r)
    
    print("\n--- REGRESSÃO (SALÁRIO) ---")
    print(f"MAE (Erro Médio Absoluto): R$ {mae:.2f}")
    print(f"RMSE (Raiz do Erro Quadrático Médio): R$ {rmse:.2f}")
    print(f"R² (Coeficiente de Determinação): {r2:.4f}")
    print("="*55 + "\n")

    os.makedirs("models", exist_ok=True)
    with open("models/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open("models/classifier.pkl", "wb") as f:
        pickle.dump(clf, f)
    with open("models/salary_regressor.pkl", "wb") as f:
        pickle.dump(reg, f)
        
    logger.info("Modelos exportados com sucesso para a pasta 'models/'!")

if __name__ == "__main__":
    main()
