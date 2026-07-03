import sqlite3

def inicializar_banco():
    # Conecta (ou cria) o arquivo do banco de dados
    conexao = sqlite3.connect('orcamentos_df.db')
    cursor = conexao.cursor()

    # Criação da Tabela de Obras (A licitação original)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS obras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_obra TEXT NOT NULL,
            regiao_administrativa TEXT NOT NULL,
            valor_inicial REAL NOT NULL,
            data_inicio TEXT
        )
    ''')

    # Criação da Tabela de Aditivos (As alterações de valor)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aditivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            obra_id INTEGER,
            valor_aditivo REAL NOT NULL,
            justificativa TEXT,
            data_aprovacao TEXT,
            FOREIGN KEY (obra_id) REFERENCES obras (id)
        )
    ''')

    conexao.commit()
    conexao.close()
    print("Banco de dados 'orcamentos_df.db' criado com sucesso! Tabelas 'obras' e 'aditivos' prontas.")

if __name__ == '__main__':
    inicializar_banco()