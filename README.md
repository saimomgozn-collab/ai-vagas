# AI Vagas 💼🤖

Uma solução inteligente e interativa de Machine Learning local e ponta a ponta para cálculo de compatibilidade de currículos (Match Score), classificação de adequação (*Fit* / *No Fit*) e análise de lacunas (*Gaps*) de competências técnicas.

O sistema opera de forma 100% off-line e local sobre bases de dados estáticas de referência em escala de mercado. O grande diferencial desta versão é o seu motor de decisão baseado em um classificador **Random Forest combinado com TF-IDF de Bigramas**, alcançando uma marca histórica de **97% de assertividade (Acurácia, Precisão e Recall)** nos testes de contratação.

---

## 🌟 Recursos e Funcionalidades

- **Inteligência Avançada (97% de Assertividade)**: Upgrade do motor linear para *Random Forest*, permitindo cruzamentos complexos e uma tomada de decisão altamente segura sobre quem é "Fit" ou "No Fit" para a vaga.
- **Análise por Bigramas**: A IA lê expressões juntas (ex: "Machine Learning", "React Native", "Data Science") em vez de palavras soltas. Isso preserva o contexto técnico real e elimina falsos positivos na triagem.
- **Matching em Escala com Dataset Real**: O motor busca vagas reais pré-filtradas da base de dados **LinkedIn Job Postings 2023-2024 (Kaggle)**, cruzando o perfil do candidato com milhares de descrições estruturadas.
- **Mapeamento de Competências Reais**: Integração com o **Job Skill Set Dataset (Kaggle)**, vinculando as competências oficiais requeridas por cargo direto ao ID de cada vaga via banco de dados SQLite.
- **Identificação Dinâmica de Gaps (Skills Faltantes)**: O matcher analisa quais das competências exigidas pela vaga estão presentes ou ausentes no currículo do usuário, gerando dicas dinâmicas para otimização do perfil.
- **Interface Streamlit Premium**: Painel visual moderno com estética Glassmorphism, suporte a upload de currículo em PDF, preenchimento direto de dados e barra de progresso interativa para importação rápida de datasets.


🚀 Como Executar o Projeto
1. Pré-requisitos
Certifique-se de ter o Python 3.10+ instalado em seu sistema.

2. Clonar e Inicializar o Ambiente
Configure o ambiente virtual local:

Bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
3. Executar o Painel Streamlit
Como os modelos com 97% de acurácia já estão prontos e salvos na pasta models/, você não precisa treinar nada para ver o sistema funcionar. Basta ligar a interface visual:

Bash
streamlit run src/app.py
Acesse no seu navegador: http://localhost:8501.

🧪 Treinamento do Modelo (Opcional)
Caso queira re-treinar a Inteligência Artificial do zero utilizando a arquitetura de Random Forest e gerar novos arquivos de calibração na pasta models/, execute:

Bash
python src/train_production.py

---

## 📂 Estrutura do Projeto

```text
ai-vagas/
├── .env                  # Configurações locais de banco (ignorado no Git)
├── .gitignore            # Proteção contra commit de chaves, caches e dados locais
├── requirements.txt      # Dependências em Python do projeto
├── README.md             # Documentação principal do sistema
├── vagas.db              # Banco de dados local SQLite contendo as vagas e competências prontas
├── models/               # Modelos preditivos (.pkl) treinados com 97% de acurácia salvos para produção
├── data/
│   ├── postings.csv      # Dataset de vagas do LinkedIn (Kaggle - ignorado no Git)
│   ├── job_skills.csv    # Dataset de mapeamento de competências (Kaggle - ignorado no Git)
│   ├── train-00000...    # Parquet de treino do Resume-JD-Match (HuggingFace - ignorado no Git)
│   └── test-00000...     # Parquet de teste do Resume-JD-Match (HuggingFace - ignorado no Git)
└── src/
    ├── app.py            # Interface gráfica Streamlit Premium com importador interativo
    ├── config.py         # Centralização de caminhos de arquivos e variáveis do .env
    ├── database.py       # Gerenciador do SQLite com importador por streaming de alto desempenho
    ├── matcher.py        # Motor de matching local que conecta o currículo ao banco via IA
    ├── train_production.py # Script responsável por processar o texto e treinar o Random Forest
    ├── seed_data.py      # Scripts iniciais de semente do banco de dados (Carga de mock data)
    └── verify_matcher.py # Script de teste funcional rápido do pipeline em modo de desenvolvimento


