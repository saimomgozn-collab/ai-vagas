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

O **AI Vagas** é uma solução inteligente e interativa de Machine Learning local e ponta a ponta para cálculo de compatibilidade de currículos (**Match Score**), classificação de adequação (**Fit/No Fit**) e análise de lacunas (**Gaps**) de competências técnicas.

O sistema opera de forma **100% offline e local** sobre bases de dados estáticas de referência em escala de mercado. O grande diferencial desta versão é o seu motor de decisão avançado baseado em um classificador **Random Forest combinado com TF-IDF de Bigramas**, alcançando uma marca histórica de **97% em todas as métricas principais** (Acurácia, Precisão, Recall e F1-Score).

> **✨ Destaque:** O banco de dados `vagas.db` já vem populado com dados reais do LinkedIn, permitindo que o sistema funcione imediatamente após a instalação, sem necessidade de baixar datasets pesados!

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

## 🚀 Guia de Instalação e Execução

### 📌 Pré-requisitos

- **Python 3.10+** instalado no sistema
- **Git** para clonar o repositório
- **Pip** para gerenciamento de pacotes

### 📥 Passo a Passo Completo

#### 1. Clone o repositório

```bash
git clone https://github.com/saimomgozn-collab/ai-vagas.git
cd ai-vagas
2. Crie e ative o ambiente virtual
bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate
3. Instale as dependências
bash
pip install -r requirements.txt
4. Execute o sistema
bash
streamlit run src/app.py
5. Acesse no navegador
text
http://localhost:8501
💡 Nota: Os modelos com 97% de acurácia já estão prontos e salvos na pasta models/. Você não precisa treinar nada para ver o sistema funcionar!

🧪 Treinamento do Modelo (Opcional)
Caso deseje retreinar a Inteligência Artificial do zero utilizando a arquitetura Random Forest e gerar novos modelos na pasta models/:

bash
python src/train_production.py
🔄 Pipeline de Treinamento
O comando acima executará automaticamente:

Pré-processamento de Dados

Limpeza e normalização de texto

Remoção de stopwords

Tokenização e extração de bigramas

Engenharia de Features

Aplicação do TF-IDF nos bigramas extraídos

Criação de matriz de características

Treinamento do Classificador

Configuração do Random Forest com otimização de hiperparâmetros

Validação cruzada para evitar overfitting

Calibração do modelo para produção

Salvamento dos Modelos

Exportação do classificador treinado (.pkl)

Salvamento do vetorizador TF-IDF

Armazenamento dos metadados de calibração

📊 Métricas de Desempenho
Métrica	Valor	Descrição
🎯 Acurácia	97%	Proporção de previsões corretas sobre o total
📈 Precisão	97%	Capacidade de não classificar incorretamente um candidato não qualificado
📉 Recall	97%	Capacidade de identificar todos os candidatos qualificados
🏆 F1-Score	97%	Média harmônica entre precisão e recall
Resultados validados em testes de contratação com dados reais do mercado.

📂 Estrutura do Projeto
text
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
🎯 Fluxo de Trabalho do Sistema









🔧 Solução de Problemas (Troubleshooting)
❌ Erro: ModuleNotFoundError
Solução: Verifique se todas as dependências foram instaladas corretamente:

bash
pip install -r requirements.txt --upgrade
❌ Erro: Port 8501 already in use
Solução: Execute o Streamlit em outra porta:

bash
streamlit run src/app.py --server.port 8502
❌ Erro: Python version not supported
Solução: Verifique sua versão do Python:

bash
python --version
Certifique-se de estar usando Python 3.10 ou superior.

❌ Erro: Database not found
Solução: O arquivo vagas.db deve estar na raiz do projeto. Se estiver faltando, execute:

bash
python src/seed_data.py
❌ Erro: MemoryError durante treinamento
Solução: Reduza a amostragem de dados no arquivo src/train_production.py:

python
# Modifique a linha de leitura do arquivo
df = pd.read_parquet('data/train-00000.parquet', nrows=5000)  # Limite de 5000 linhas
❌ Erro: FileNotFoundError para datasets
Solução: Certifique-se de que os datasets estão no local correto. Caso não os tenha, o sistema usará os dados de mock do seed_data.py.

🛠️ Tecnologias e Dependências
Core Stack
Tecnologia	Versão	Finalidade
Python	3.10+	Linguagem principal
Streamlit	1.28+	Interface visual interativa
Scikit-learn	1.3+	Random Forest, TF-IDF e métricas
SQLite	3+	Banco de dados local
Pandas	2.0+	Manipulação e análise de dados
NumPy	1.24+	Computação numérica
Bibliotecas de Suporte
Biblioteca	Finalidade
PyPDF2	Extração de texto de currículos PDF
NLTK	Processamento de linguagem natural
Joblib	Serialização de modelos
Python-dotenv	Gerenciamento de variáveis de ambiente
Plotly	Visualizações interativas
🤝 Contribuindo
Contribuições são bem-vindas! Siga os passos abaixo:

Como Contribuir
Fork o projeto

Crie sua branch (git checkout -b feature/AmazingFeature)

Commit suas mudanças (git commit -m 'Add some AmazingFeature')

Push para a branch (git push origin feature/AmazingFeature)

Abra um Pull Request

Diretrizes de Contribuição
Mantenha a compatibilidade com Python 3.10+

Adicione testes para novas funcionalidades

Documente claramente suas alterações

Siga o estilo de código PEP 8

Atualize o README se necessário

📄 Licença
Distribuído sob a licença MIT. Veja o arquivo LICENSE para mais informações.

text
MIT License

Copyright (c) 2024 Saimom Gozn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
📧 Contato e Suporte
Autor: Saimom Gozn

Links Úteis:

🔗 Repositório do Projeto

🐛 Reportar Bug

💡 Sugerir Funcionalidade

Suporte:

Para dúvidas técnicas, abra uma Issue

Para contribuições, siga as diretrizes acima

Para suporte rápido, consulte a seção de Troubleshooting

📊 Roadmap Futuro
✅ Funcionalidades Implementadas
Sistema de match com Random Forest

Análise de gaps de competências

Interface Streamlit premium

Upload de currículos em PDF

Banco de dados SQLite integrado

🚀 Próximos Passos
Suporte a múltiplos idiomas (EN/PT-BR)

API REST para integração com sistemas externos

Dashboard com análises estatísticas avançadas

Exportação de relatórios em PDF

Integração com LinkedIn API

Sistema de recomendações de cursos para gaps identificados

<div align="center">
⭐ Mostre seu Apoio
Feito com ❤️ por Saimom Gozn

Se este projeto te ajudou ou te inspirou, não se esqueça de:

🌟 Dar uma estrela no GitHub
👥 Compartilhar com outros desenvolvedores
📝 Deixar seu feedback

"Transformando dados em oportunidades de carreira com inteligência artificial"

</div> ```
📝 Principais Ajustes Realizados
✅ Correções de Formatação
Adicionei os delimitadores de código (```) em todos os blocos

Corrigi a indentação dos passos de instalação

Formatei corretamente as listas e subitens

✅ Adições Importantes
Incluí o Fluxograma Mermaid que estava faltando

Adicionei os emojis nos títulos das seções

Formatei a estrutura de pastas com identação correta

✅ Organização Visual
Todos os comandos estão em blocos de código com linguagem especificada

As tabelas estão perfeitamente alinhadas

Os destaques estão com ícones e formatação adequada
