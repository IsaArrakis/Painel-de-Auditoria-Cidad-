import sqlite3
import pandas as pd
import os

def limpar_e_converter_valor(valor_str):
    """Limpa a formatação de moeda brasileira do CSV para o padrão do banco (Float)"""
    if pd.isna(valor_str) or str(valor_str).strip() == "":
        return 0.0
    try:
        s = str(valor_str).replace("R$", "").strip()
        s = s.replace(".", "")   # Remove os pontos de milhar
        s = s.replace(",", ".")  # Troca a vírgula decimal por ponto
        return float(s)
    except ValueError:
        return 0.0

def importar_dados_gdf(caminho_csv):
    if not os.path.exists(caminho_csv):
        print(f"[!] Erro: O arquivo {caminho_csv} não foi encontrado.")
        return False

    print("[+] Lendo arquivo CSV do GDF...")
    
    # O segredo está aqui: skiprows=1 ignora a primeira linha suja do CSV
    df_gov = pd.read_csv(caminho_csv, sep=';', encoding='utf-8', skiprows=1, dtype=str)

    # Limpando espaços em branco nos nomes das colunas (comum em arquivos do governo)
    df_gov.columns = df_gov.columns.str.strip()

    # --- NOVO MAPEAMENTO DE COLUNAS BASEADO NA SUA IMAGEM ---
    coluna_nome = 'Ação' 
    coluna_local = 'Unidade Gestora'
    coluna_valor_inicial = 'Empenhado'
    coluna_valor_final = 'Total Pago' 

    conn = sqlite3.connect('orcamentos_df.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS obras (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_obra TEXT, regiao_administrativa TEXT, valor_inicial REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS aditivos (id INTEGER PRIMARY KEY AUTOINCREMENT, obra_id INTEGER, valor_aditivo REAL, justificativa TEXT, FOREIGN KEY (obra_id) REFERENCES obras (id))''')
    
    # Limpa o banco antigo
    cursor.execute("DELETE FROM aditivos")
    cursor.execute("DELETE FROM obras")
    conn.commit()

    registros_inseridos = 0

    print("[+] Injetando dados reais no banco SQLite...")
    for _, linha in df_gov.iterrows():
        try:
            # Pula linhas vazias ou mal formatadas
            if pd.isna(linha.get(coluna_nome)):
                continue

            nome = str(linha[coluna_nome])[:150]
            localidade = str(linha.get(coluna_local, "GDF"))
            
            val_inicial = limpar_e_converter_valor(linha.get(coluna_valor_inicial, 0))
            val_final = limpar_e_converter_valor(linha.get(coluna_valor_final, 0))
            
            # Na contabilidade pública, se o Total Pago for maior que o Empenhado inicial, consideramos como Aditivo
            diferenca_aditivo = val_final - val_inicial

            cursor.execute('INSERT INTO obras (nome_obra, regiao_administrativa, valor_inicial) VALUES (?, ?, ?)', (nome, localidade, val_inicial))
            obra_id = cursor.lastrowid

            if diferenca_aditivo > 0:
                cursor.execute('INSERT INTO aditivos (obra_id, valor_aditivo, justificativa) VALUES (?, ?, ?)', (obra_id, diferenca_aditivo, 'Variação na execução contratual'))

            registros_inseridos += 1
            
        except Exception as e:
            continue

    conn.commit()
    conn.close()
    print(f"[🚀] Sucesso! {registros_inseridos} contratos do DF foram importados com sucesso.")
    return True

if __name__ == '__main__':
    importar_dados_gdf('contratos_federais.csv')