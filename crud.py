import sqlite3

# --- CONFIGURAÇÃO ---
def conectar():
    return sqlite3.connect('orcamentos_df.db')

# --- CREATE (Inserir Dados) ---
def inserir_obra(nome, regiao, valor_inicial):
    sucesso = False # Variável booleana para controle de fluxo
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO obras (nome_obra, regiao_administrativa, valor_inicial)
            VALUES (?, ?, ?)
        ''', (nome, regiao, valor_inicial))
        conn.commit()
        sucesso = True
        print(f"[+] Obra '{nome}' registrada com sucesso.")
    except Exception as e:
        print(f"[!] Erro ao inserir obra: {e}")
    finally:
        conn.close()
        return sucesso

def inserir_aditivo(obra_id, valor, justificativa):
    sucesso = False
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO aditivos (obra_id, valor_aditivo, justificativa)
            VALUES (?, ?, ?)
        ''', (obra_id, valor, justificativa))
        conn.commit()
        sucesso = True
        print(f"[+] Aditivo de R$ {valor:,.2f} aplicado à obra ID {obra_id}.")
    except Exception as e:
        print(f"[!] Erro ao inserir aditivo: {e}")
    finally:
        conn.close()
        return sucesso

# --- READ (Ler e Processar Dados) ---
def listar_resumo_obras():
    conn = conectar()
    cursor = conn.cursor()
    
    # Esta query cruza as tabelas e soma os aditivos automaticamente
    cursor.execute('''
        SELECT 
            o.id, 
            o.nome_obra, 
            o.valor_inicial,
            COALESCE(SUM(a.valor_aditivo), 0) as total_aditivos,
            (o.valor_inicial + COALESCE(SUM(a.valor_aditivo), 0)) as custo_final
        FROM obras o
        LEFT JOIN aditivos a ON o.id = a.obra_id
        GROUP BY o.id
    ''')
    resultados = cursor.fetchall()
    conn.close()

    print("\n" + "="*40)
    print("      RESUMO DE EXECUÇÃO FINANCEIRA      ")
    print("="*40)
    
    for linha in resultados:
        print(f"ID {linha[0]} | {linha[1]}")
        print(f"  Orçamento Previsto: R$ {linha[2]:,.2f}")
        print(f"  Soma de Aditivos:   R$ {linha[3]:,.2f}")
        print(f"  CUSTO FINAL:        R$ {linha[4]:,.2f}")
        print("-" * 40)

# --- EXECUÇÃO (Maestro) ---
if __name__ == '__main__':
    print("Iniciando injeção de dados de teste...\n")

    # 1. Criando obras baseadas na realidade do DF
    inserir_obra('Expansão da Linha do Metrô', 'Ceilândia', 50000000.00)
    inserir_obra('Reforma do HRAN', 'Plano Piloto', 12000000.00)

    # 2. Aplicando os aditivos (estourando o orçamento da primeira obra)
    inserir_aditivo(1, 5000000.00, 'Reajuste no preço do aço e concreto')
    inserir_aditivo(1, 2500000.00, 'Extensão de prazo por chuvas')
    inserir_aditivo(2, 3000000.00, 'Ampliação emergencial da UTI')

    # 3. Exibindo o resultado final processado
    listar_resumo_obras()