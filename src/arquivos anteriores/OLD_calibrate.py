import os
import re
import numpy as np
from pathlib import Path
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import cross_val_predict
from sklearn.linear_model import LogisticRegression
from sentence_transformers import SentenceTransformer
from loguru import logger

def extract_job_and_resume(text: str) -> tuple:
    # fatiamento do texto
    jd_pattern = re.compile(r"job description\s*<<+(.*?)>>+\s*the\s*resume:", re.IGNORECASE | re.DOTALL)
    res_pattern = re.compile(r"the\s*resume:\s*<<+(.*?)(?:>>+\s*\.\s*the|>>+\s*$)", re.IGNORECASE | re.DOTALL)
    
    jd_match = jd_pattern.search(text)
    res_match = res_pattern.search(text)
    
    if jd_match and res_match:
        return jd_match.group(1).strip(), res_match.group(1).strip()
        
    if "<<" in text:
        parts = text.split("<<")
        if len(parts) >= 3:
            return parts[1].split(">>")[0].strip(), parts[2].split(">>")[0].strip()
            
    return "", ""

def run_self_cleaning_pipeline():
    train_path = Path("data/train-00000-of-00001.parquet")
    test_path = Path("data/test-00000-of-00001.parquet")
    import pandas as pd
    
    # carrega dados brutos
    logger.info("Carregando bases originais...")
    df_train = pd.read_parquet(train_path).sample(n=2000, random_state=42)
    df_test = pd.read_parquet(test_path).sample(n=500, random_state=42)
    
    # processa extracao treino
    train_jds, train_res, y_train_raw = [], [], []
    for _, row in df_train.iterrows():
        jd, res = extract_job_and_resume(str(row['text']))
        if jd and res:
            train_jds.append(jd)
            train_res.append(res)
            label = str(row['label']).strip().lower()
            y_train_raw.append(1 if label in ['1', 'true', 'fit', 'match', 'potential fit', 'good fit'] else 0)
            
    # processa extracao teste
    test_jds, test_res, y_test = [], [], []
    for _, row in df_test.iterrows():
        jd, res = extract_job_and_resume(str(row['text']))
        if jd and res:
            test_jds.append(jd)
            test_res.append(res)
            label = str(row['label']).strip().lower()
            y_test.append(1 if label in ['1', 'true', 'fit', 'match', 'potential fit', 'good fit'] else 0)

    # converte semantica vetorial
    logger.info("Extraindo semantica vetorial...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    emb_jds_train = model.encode(train_jds, convert_to_numpy=True, show_progress_bar=False)
    emb_res_train = model.encode(train_res, convert_to_numpy=True, show_progress_bar=False)
    X_train_raw = np.hstack((emb_jds_train, emb_res_train)) # concatena representacoes
    
    emb_jds_test = model.encode(test_jds, convert_to_numpy=True, show_progress_bar=False)
    emb_res_test = model.encode(test_res, convert_to_numpy=True, show_progress_bar=False)
    X_test = np.hstack((emb_jds_test, emb_res_test))

    # fase auditoria dados
    logger.info("Iniciando self-cleaning local...")
    clf_auditor = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
    
    # previsao cruzada isenta
    cv_probs = cross_val_predict(clf_auditor, X_train_raw, y_train_raw, cv=5, method='predict_proba')[:, 1]
    
    # calcula divergencia erro
    y_train_arr = np.array(y_train_raw)
    diffs = np.abs(cv_probs - y_train_arr)
    
    # remove inconsistencias graves
    clean_mask = diffs < 0.65
    X_train_clean = X_train_raw[clean_mask]
    y_train_clean = y_train_arr[clean_mask]
    
    removidos = len(y_train_arr) - sum(clean_mask)
    logger.info(f"Filtro aplicado. {removidos} registros corrompidos removidos do treino.")

    # treina modelo definitivo
    logger.info("Treinando em dados limpos...")
    clf_final = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
    clf_final.fit(X_train_clean, y_train_clean)
    
    # validacao base teste
    preds = clf_final.predict(X_test)
    acc = accuracy_score(y_test, preds)
    
    logger.info("-" * 60)
    logger.info(f"SISTEMA AUTO-LIMPANTE: TREINO SEM RUÍDO")
    logger.info(f"Acurácia contra Gabarito (que pode conter erro): {acc * 100:.1f}%")
    logger.info("-" * 60)
    
    report = classification_report(y_test, preds, target_names=["No Fit (0)", "Fit (1)"], zero_division=0)
    print(report)

if __name__ == "__main__":
    # executa auto limpeza
    run_self_cleaning_pipeline()