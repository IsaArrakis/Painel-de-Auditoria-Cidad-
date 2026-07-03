import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# 1. CONFIGURAÇÃO VISUAL E CSS CUSTOMIZADO
# ==========================================
st.set_page_config(page_title="Auditoria Cidadã", layout="wide", page_icon="👁️")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 3rem; padding-bottom: 0rem;}
    
    /* Tipografia Gigante para a página inicial */
    .big-font {
        font-size: 65px !important;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 15px;
        letter-spacing: -1px;
    }
    .sub-font {
        font-size: 24px !important;
        color: #A0A0A0;
        margin-bottom: 40px;
        font-family: sans-serif;
    }
    /* Estilo para os Grandes Números */
    .metric-value {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 0px;
        line-height: 1;
    }
    .metric-label {
        color: #888888;
        font-size: 1rem;
        margin-top: 5px;
        font-family: sans-serif;
    }
    .highlight-red { color: #E63946; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. FUNÇÕES DE DADOS
# ==========================================
@st.cache_data
def carregar_dados():
    try:
        conn = sqlite3.connect('orcamentos_df.db')
        query = '''
            SELECT 
                o.nome_obra, 
                o.regiao_administrativa,
                o.valor_inicial,
                COALESCE(SUM(a.valor_aditivo), 0) as total_aditivos,
                (o.valor_inicial + COALESCE(SUM(a.valor_aditivo), 0)) as custo_final
            FROM obras o
            LEFT JOIN aditivos a ON o.id = a.obra_id
            GROUP BY o.id
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        if not df.empty:
            df['variacao_pct'] = ((df['custo_final'] / df['valor_inicial']) - 1) * 100
            df['variacao_pct'] = df['variacao_pct'].fillna(0)
        return df
    except Exception:
        return pd.DataFrame()

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# ==========================================
# 3. GERENCIAMENTO DE ESTADO E INICIALIZAÇÃO
# ==========================================
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'marketing'
if 'regioes_selecionadas' not in st.session_state:
    st.session_state['regioes_selecionadas'] = []

df = carregar_dados()

# Verifica se o banco está vazio
if df.empty:
    st.error("Banco de dados vazio ou não encontrado. Execute o script de importação primeiro.")
    st.stop()

# Pega todos os órgãos e organiza em ordem alfabética
todas_regioes = sorted(df['regiao_administrativa'].unique().tolist())

# ==========================================
# PÁGINA 1: MARKETING (HOME)
# ==========================================
if st.session_state['pagina'] == 'marketing':
    
    col_spacer1, col_center, col_spacer2 = st.columns([1, 3, 1])
    
    with col_center:
        st.markdown('<p class="big-font">Auditoria cidadã<br>de ponta a ponta.</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-font">Acompanhe como o dinheiro público sofre mutações através de aditivos contratuais em projetos pelo DF.</p>', unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### Selecione os Órgãos Responsáveis para fiscalizar:")
        
        # O novo Menu Suspenso Inteligente
        selecoes = st.multiselect(
            "Órgãos Governamentais (Unidades Gestoras):",
            options=todas_regioes,
            default=todas_regioes[:4] if len(todas_regioes) >= 4 else todas_regioes,
            placeholder="Clique aqui para buscar um órgão específico (ex: NOVACAP, DER)..."
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("ACESSAR DADOS ➜", type="primary", use_container_width=True):
            st.session_state['regioes_selecionadas'] = selecoes
            st.session_state['pagina'] = 'dashboard'
            st.rerun()

# ==========================================
# PÁGINA 2: DASHBOARD (NÚMEROS E TABELA)
# ==========================================
elif st.session_state['pagina'] == 'dashboard':
    
    if st.button("← VOLTAR"):
        st.session_state['pagina'] = 'marketing'
        st.rerun()

    df_filtrado = df[df['regiao_administrativa'].isin(st.session_state['regioes_selecionadas'])].copy()

    # Grandes Números 
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### RESULTADO DA AUDITORIA", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<p class='metric-value'>{formatar_moeda(df_filtrado['valor_inicial'].sum())}</p>", unsafe_allow_html=True)
        st.markdown("<p class='metric-label'>Total orçado nas licitações originais</p>", unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"<p class='metric-value highlight-red'>{formatar_moeda(df_filtrado['total_aditivos'].sum())}</p>", unsafe_allow_html=True)
        st.markdown("<p class='metric-label'>Encontrados em aditivos contratuais</p>", unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"<p class='metric-value'>{formatar_moeda(df_filtrado['custo_final'].sum())}</p>", unsafe_allow_html=True)
        st.markdown("<p class='metric-label'>Custo atualizado suportado pelos cofres públicos</p>", unsafe_allow_html=True)

    st.divider()

    # Preparação da Tabela (Limpeza dos Zeros)
    df_exibicao = df_filtrado.copy()
    df_exibicao['valor_inicial'] = df_exibicao['valor_inicial'].apply(formatar_moeda)
    df_exibicao['total_aditivos'] = df_exibicao['total_aditivos'].apply(formatar_moeda)
    df_exibicao['custo_final'] = df_exibicao['custo_final'].apply(formatar_moeda)

    st.markdown("### Detalhamento por Contrato")
    st.dataframe(
        df_exibicao,
        column_config={
            "nome_obra": st.column_config.TextColumn("Objeto/Projeto", width="large"),
            "regiao_administrativa": "Órgão Gestor",
            "valor_inicial": "Valor Inicial",
            "total_aditivos": "Soma de Aditivos",
            "custo_final": "Valor Atualizado",
            "variacao_pct": st.column_config.NumberColumn("Desvio (%)", format="%.1f %%")
        },
        hide_index=True,
        use_container_width=True
    )