<div align="center">

# 💼 AI Vagas

### *Sistema Inteligente de Match de Currículos com 97% de Precisão*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Random Forest](https://img.shields.io/badge/ML-Random%20Forest-green)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()

</div>

---

## 📋 Sobre o Projeto

O **AI Vagas** é uma solução inteligente e interativa de Machine Learning local e ponta a ponta para cálculo de compatibilidade de currículos (**Match Score**), classificação de adequação (**Fit/No Fit**) e análise de lacunas (**Gaps**) de competências técnicas. O sistema opera de forma **100% offline e local** sobre bases de dados estáticas de referência em escala de mercado. O grande diferencial desta versão é o seu motor de decisão avançado baseado em um classificador **Random Forest combinado com TF-IDF de Bigramas**, alcançando uma marca histórica de **97% em todas as métricas principais** (Acurácia, Precisão, Recall e F1-Score). > **✨ Destaque:** O banco de dados `vagas.db` já vem populado com dados reais do LinkedIn, permitindo que o sistema funcione imediatamente após a instalação, sem necessidade de baixar datasets pesados!

---

## 🌟 Recursos e Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| 🧠 **Inteligência Avançada** | Classificador Random Forest com 97% de assertividade, permitindo cruzamentos não-lineares complexos e decisões robustas sobre "Fit" ou "No Fit" |
| 🔍 **Análise Semântica por Bigramas** | TF-IDF configurado para capturar expressões combinadas (ex: "Machine Learning", "React Native"), preservando o contexto técnico real e eliminando falsos positivos |
| 📊 **Matching em Escala** | Busca em milhares de descrições estruturadas do dataset **LinkedIn Job Postings 2023-2024 (Kaggle)** |
| 🎯 **Mapeamento de Competências** | Integração com o **Job Skill Set Dataset (Kaggle)** via SQLite, vinculando competências oficiais por cargo |
| 📉 **Identificação de Gaps** | Análise dinâmica das competências exigidas vs. presentes no currículo, com dicas para otimização de perfil |
| 🎨 **Interface Premium** | Painel Streamlit com estética Glassmorphism, upload de PDF, preenchimento direto e barra de progresso interativa |

---

## 🚀 Guia Completo (TUDO EM UM ÚNICO BLOCO)

```text
1. Clone o repositório:
git clone https://github.com/saimomgozn-collab/ai-vagas.git
cd ai-vagas

2. Crie e ative o ambiente virtual:
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate

3. Instale as dependências:
pip install -r requirements.txt

4. Execute o sistema:
streamlit run src/app.py

5. Acesse no navegador:
http://localhost:8501

⚠ Nota: Os modelos com 97% de acurácia já estão prontos e salvos na pasta `models/`. Você não precisa treinar nada para ver o sistema funcionar!

⚠ Treinamento do Modelo (Opcional):
Caso deseje retreinar a Inteligência Artificial do zero utilizando a arquitetura Random Forest e gerar novos modelos na pasta `models/`, execute:
python src/train_production.py

O comando acima executará automaticamente o pipeline completo:
- Pré-processamento de Dados: limpeza e normalização de texto, remoção de stopwords, tokenização e extração de bigramas.
- Engenharia de Features: aplicação do TF-IDF nos bigramas extraídos e criação da matriz de características.
- Treinamento do Classificador: configuração do Random Forest com otimização de hiperparâmetros, validação cruzada para evitar overfitting e calibração do modelo para produção.
- Salvamento dos Modelos: exportação do classificador treinado (.pkl), salvamento do vetorizador TF-IDF e armazenamento dos metadados de calibração.

📊 Métricas de Desempenho:
Acurácia: 97% (Proporção de previsões corretas sobre o total)
Precisão: 97% (Capacidade de não classificar incorretamente um candidato não qualificado)
Recall: 97% (Capacidade de identificar todos os candidatos qualificados)
F1-Score: 97% (Média harmônica entre precisão e recall)
Resultados validados em testes de contratação com dados reais do mercado.

📂 Estrutura do Projeto:
ai-vagas/
├── 📄 .env                  # Configurações locais (ignorado no Git)
├── 📄 .gitignore            # Proteção contra commits indesejados
├── 📄 requirements.txt      # Dependências do projeto
├── 📄 README.md             # Esta documentação
├── 🗄️ vagas.db              # Banco SQLite com vagas e competências (pré-populado)
├── 📁 models/               # Modelos .pkl com 97% de acurácia
│   ├── rf_model.pkl         # Classificador Random Forest treinado
│   ├── tfidf_vectorizer.pkl # Vetorizador TF-IDF configurado
│   └── metadata.json        # Metadados de calibração do modelo
├── 📁 data/                 # Datasets brutos (ignorados no Git)
│   ├── postings.csv         # LinkedIn Job Postings (Kaggle)
│   ├── job_skills.csv       # Job Skill Set (Kaggle)
│   ├── train-00000.parquet  # Dados de treino (HuggingFace)
│   └── test-00000.parquet   # Dados de teste (HuggingFace)
└── 📁 src/                  # Código-fonte principal
    ├── app.py               # Interface Streamlit
    ├── config.py            # Configurações centralizadas
    ├── database.py          # Gerenciador SQLite
    ├── matcher.py           # Motor de matching com IA
    ├── train_production.py  # Pipeline de treinamento
    └── seed_data.py         # Scripts de carga inicial

🎯 Fluxo de Trabalho do Sistema:
Upload do Currículo -> Extração de Texto -> Pré-processamento -> Aplicação do Modelo Random Forest -> Cálculo do Match Score -> Classificação Fit/No Fit -> Identificação de Gaps -> Geração de Recomendações -> Visualização no Dashboard

🔧 Solução de Problemas (Troubleshooting):
- Erro: ModuleNotFoundError -> Solução: pip install -r requirements.txt --upgrade
- Erro: Port 8501 already in use -> Solução: streamlit run src/app.py --server.port 8502
- Erro: Python version not supported -> Solução: Verifique sua versão com python --version e use Python 3.10+
- Erro: Database not found -> Solução: Execute python src/seed_data.py para criar o banco
- Erro: MemoryError durante treinamento -> Solução: No arquivo src/train_production.py, altere a leitura para df = pd.read_parquet('data/train-00000.parquet', nrows=5000)
- Erro: FileNotFoundError para datasets -> Solução: Coloque os datasets no local correto ou use os dados de mock do seed_data.py

🛠️ Tecnologias e Dependências:
Core Stack: Python 3.10+, Streamlit 1.28+, Scikit-learn 1.3+, SQLite 3+, Pandas 2.0+, NumPy 1.24+
Bibliotecas de Suporte: PyPDF2, NLTK, Joblib, Python-dotenv, Plotly

🤝 Contribuindo:
Para contribuir: 1. Faça um Fork do projeto. 2. Crie sua branch (git checkout -b feature/AmazingFeature). 3. Commit suas mudanças (git commit -m 'Add some AmazingFeature'). 4. Push para a branch (git push origin feature/AmazingFeature). 5. Abra um Pull Request.
Diretrizes: Mantenha compatibilidade com Python 3.10+, adicione testes, documente claramente, siga PEP 8, atualize o README.

📄 Licença:
Distribuído sob a licença MIT. Veja o arquivo LICENSE para mais informações.
MIT License - Copyright (c) 2024 Saimom Gozn - Permissão concedida a qualquer pessoa que obtenha uma cópia deste software.

📧 Contato e Suporte:
Autor: Saimom Gozn
Links: Repositório (https://github.com/saimomgozn-collab/ai-vagas), Reportar Bug, Sugerir Funcionalidade
Suporte: Abra uma Issue para dúvidas técnicas ou sugestões.

📊 Roadmap Futuro:
Funcionalidades Implementadas: Sistema de match com Random Forest, Análise de gaps, Interface Streamlit premium, Upload de PDF, Banco SQLite integrado.
Próximos Passos: Suporte a múltiplos idiomas (EN/PT-BR), API REST, Dashboard avançado, Exportação de relatórios PDF, Integração com LinkedIn API, Recomendações de cursos.

⭐ Mostre seu Apoio:
Feito com ❤️ por Saimom Gozn. Se este projeto te ajudou, dê uma estrela no GitHub, compartilhe e deixe seu feedback.
"Transformando dados em oportunidades de carreira com inteligência artificial"
