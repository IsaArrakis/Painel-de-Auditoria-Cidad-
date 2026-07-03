# 👁️ Painel de Auditoria Cidadã - Obras DF

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)

Um painel de inteligência de dados com design minimalista focado na transparência dos gastos públicos no Distrito Federal. O sistema extrai dados abertos do governo, processa as informações e cruza os orçamentos iniciais licitados com o custo final atualizado, revelando o impacto dos aditivos contratuais.

## 🎯 Objetivo
Transformar dados governamentais complexos e dispersos em informações visuais e acessíveis. O projeto permite que qualquer cidadão audite a evolução financeira das obras executadas por diferentes órgãos gestores (como NOVACAP, DER/DF e Secretarias), identificando rapidamente desvios e aumentos de custo.

## ✨ Funcionalidades
* **Pipeline ETL Automatizado:** Script nativo para limpar e estruturar planilhas brutas em CSV fornecidas pelo Portal da Transparência do GDF.
* **Banco de Dados Relacional:** Armazenamento eficiente utilizando SQLite, separando dados de obras e aditivos financeiros.
* **Interface Dark Mode:** UI focada em legibilidade e alto contraste, inspirada em plataformas de auditoria cívica.
* **Filtros Dinâmicos:** Seleção inteligente por Órgão Gestor, recalculando automaticamente os indicadores globais (KPIs).

## 🚀 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Python instalado na sua máquina. É recomendável utilizar um ambiente virtual.

```bash
# Clone este repositório
git clone [https://github.com/SEU_USUARIO/painel-obras-df.git](https://github.com/SEU_USUARIO/painel-obras-df.git)

# Entre no diretório
cd painel-obras-df

# Crie e ative um ambiente virtual (Linux/macOS)
python3 -m venv venv
source venv/bin/activate
