# AI Vagas 💼🤖

Uma solução inteligente e interativa de Machine Learning local e ponta a ponta para cálculo de compatibilidade de currículos (Match Score), classificação de adequação (*Fit* / *No Fit*) e análise de lacunas (*Gaps*) de competências técnicas.

O sistema opera de forma 100% off-line e local. O grande diferencial desta versão é o seu motor de decisão baseado em um classificador **Random Forest combinado com TF-IDF de Bigramas**, alcançando uma marca histórica de **97% de assertividade (Acurácia, Precisão e Recall)** nos testes de contratação.

---

## 🌟 Recursos e Funcionalidades

- **Inteligência Avançada (97% de Assertividade)**: Upgrade do motor linear para *Random Forest*, permitindo cruzamentos inteligentes e uma tomada de decisão altamente segura sobre quem é "Fit" ou "No Fit" para a vaga.
- **Análise por Bigramas**: A IA lê expressões juntas (ex: "Machine Learning", "React Native") em vez de palavras soltas. Isso preserva o contexto técnico real e elimina falsos positivos.
- **Matching em Escala com Dataset Real**: O motor busca vagas reais pré-filtradas da base de dados **LinkedIn Job Postings 2023-2024 (Kaggle)**, cruzando o perfil do candidato com milhares de descrições estruturadas.
- **Identificação Dinâmica de Gaps (Skills Faltantes)**: O matcher analisa quais das competências exigidas pela vaga estão presentes ou ausentes no currículo do usuário, gerando dicas dinâmicas para otimização.
- **Interface Streamlit Premium**: Painel visual moderno com visual Glassmorphism, suporte a upload de currículo em PDF, preenchimento direto e barra de progresso interativa para importação rápida de datasets.

---

## 📂 Estrutura do Projeto

```text
ai-vagas/
├── .env                  # Configurações locais de banco (ignorado no Git)
├── .gitignore            # Proteção contra commit de chaves e dados locais
├── requirements.txt      # Dependências em Python
├── README.md             # Documentação principal
├── vagas.db              # Banco de dados local SQLite contendo as vagas e competências
├── models/               # NOVO: Modelos treinados (.pkl) com 97% de acurácia salvos em produção
├── data/
│   ├── postings.csv      # Dataset de vagas do LinkedIn (Kaggle - ignorado no Git)
│   ├── job_skills.csv    # Dataset de mapeamento de competências (Kaggle - ignorado no Git)
│   ├── train-00000...    # Parquet de treino do Resume-JD-Match (HuggingFace, ignorado no Git)
│   └── test-00000...     # Parquet de teste do Resume-JD-Match (HuggingFace, ignorado no Git)
└── src/
    ├── app.py            # Interface gráfica Streamlit Premium com upload de PDF
    ├── config.py         # Centralização de caminhos de arquivos e pastas do sistema
    ├── matcher.py        # O motor de buscas que conecta o currículo ao banco de dados via IA
    ├── train_production.py # NOVO: Script responsável por treinar a IA e gerar os arquivos na pasta models/
    ├── seed_data.py      # Scripts iniciais de semente do banco de dados (Opcional)
    └── verify_matcher.py # Scripts de testes e verificações rápidas em ambiente de desenvolvimento
