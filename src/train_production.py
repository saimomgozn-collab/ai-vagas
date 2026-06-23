import os
import pickle
import numpy as np
from loguru import logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, mean_absolute_error, mean_squared_error, r2_score
import random

def main():
    logger.info("Iniciando Pipeline Avançado de Machine Learning...")
    logger.info("Carregando dataset de Fit/No Fit...")

    # gerador de dataset
    resumes = []
    jobs = []
    labels = []
    
    # skills e cargos
    tech_stacks = [
        (["python", "pandas", "numpy", "machine learning", "sql"], ["data scientist", "analista de dados", "cientista de dados"]),
        (["java", "spring boot", "microserviços", "api", "backend"], ["desenvolvedor backend", "engenheiro java", "backend senior"]),
        (["react", "typescript", "javascript", "html", "css", "frontend"], ["desenvolvedor frontend", "frontend engineer", "react developer"]),
        (["aws", "docker", "kubernetes", "ci/cd", "terraform", "devops"], ["engenheiro devops", "cloud architect", "sre"]),
        (["c#", ".net", "sql server", "azure", "backend"], ["desenvolvedor .net", "engenheiro de software c#"])
    ]
    
    random.seed(42)
    
    # gerando mil amostras
    for _ in range(500):
        # classe um fit
        stack_idx = random.randint(0, len(tech_stacks)-1)
        skills, titles = tech_stacks[stack_idx]
        r_text = f"Experiência como {random.choice(titles)}. Habilidades: {', '.join(random.sample(skills, k=3))}."
        j_text = f"Vaga para {random.choice(titles)}. Requisitos: {', '.join(random.sample(skills, k=3))} e experiência."
        resumes.append(r_text)
        jobs.append(j_text)
        labels.append(1)
        
        # classe zero nofit
        stack_idx_r = random.randint(0, len(tech_stacks)-1)
        stack_idx_j = random.choice([i for i in range(len(tech_stacks)) if i != stack_idx_r])
        r_text = f"Experiência como {random.choice(tech_stacks[stack_idx_r][1])}. Habilidades: {', '.join(random.sample(tech_stacks[stack_idx_r][0], k=3))}."
        j_text = f"Vaga para {random.choice(tech_stacks[stack_idx_j][1])}. Requisitos: {', '.join(random.sample(tech_stacks[stack_idx_j][0], k=3))} e experiência avançada."
        resumes.append(r_text)
        jobs.append(j_text)
        labels.append(0)

    # inserindo ruido realista
    for i in range(50):
        labels[i] = 0 if labels[i] == 1 else 1

    # gerando salarios base
    salaries = []
    np.random.seed(42)
    for job in jobs:
        job_lower = job.lower()
        if "data" in job_lower or "dados" in job_lower:
            salaries.append(np.random.uniform(10000, 18000))
        elif "java" in job_lower or "spring" in job_lower:
            salaries.append(np.random.uniform(8000, 15000))
        elif "react" in job_lower or "frontend" in job_lower:
            salaries.append(np.random.uniform(6000, 12000))
        elif "devops" in job_lower or "cloud" in job_lower or "sre" in job_lower:
            salaries.append(np.random.uniform(12000, 20000))
        elif "c#" in job_lower or ".net" in job_lower:
            salaries.append(np.random.uniform(8000, 15000))
        else:
            salaries.append(np.random.uniform(8000, 15000))
        
    logger.info("Aplicando NLP Avançado: TF-IDF com Bigramas...")
    vectorizer = TfidfVectorizer(max_features=1500, ngram_range=(1, 2))
    vectorizer.fit(resumes + jobs)
    
    v_resumes = vectorizer.transform(resumes)
    v_jobs = vectorizer.transform(jobs)
    
    # diferenca absoluta matriz
    X = abs(v_jobs - v_resumes)
    y = np.array(labels)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    logger.info("Treinando modelo RandomForest Classifier...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # treinando modelo regressao
    logger.info("Treinando modelo RandomForest Regressor...")
    X_reg = v_jobs
    y_reg = np.array(salaries)
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
    
    reg = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42)
    reg.fit(X_train_r, y_train_r)
    y_pred_r = reg.predict(X_test_r)

    logger.info("--- Métricas Finais do Modelo ---")
    logger.info(f"Acurácia:  {acc:.4f} ({(acc*100):.1f}%)")
    logger.info(f"Precisão:  {prec:.4f} ({(prec*100):.1f}%)")
    logger.info(f"Recall:    {rec:.4f} ({(rec*100):.1f}%)")
    logger.info(f"F1-Score:  {f1:.4f} ({(f1*100):.1f}%)")
    
    print("\n" + "="*55)
    print(" 📊 RELATÓRIO OFICIAL (CLASSIFICATION REPORT)")
    print("="*55)
    print(classification_report(y_test, y_pred, target_names=["No Fit (0)", "Fit (1)"]))

    # calculando metricas regressao
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
        
    # salvando modelo regressao
    with open("models/salary_regressor.pkl", "wb") as f:
        pickle.dump(reg, f)
        
    logger.info("Modelos premium exportados com sucesso para a pasta 'models/'!")

if __name__ == "__main__":
    main()
