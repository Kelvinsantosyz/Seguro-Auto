import pymysql
import pandas as pd
import os
from Extrair_dados import extrair_texto_pdf, extrair_dados_contrato, gerar_hash_pdf  # Importando funções do módulo

# Diretório dos PDFs
diretorio_pdf = r"C:\Users\Kelvin\Desktop\Projeto"

# Conectar ao MySQL
try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="305614",
        database="seu_banco_de_dados",
        autocommit=True
    )
    cursor = conn.cursor()

    # Criar tabela se não existir
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS vendas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        marca VARCHAR(255),
        modelo VARCHAR(255),
        ano INT,
        cor VARCHAR(50),
        valor_mensal FLOAT,
        duracao INT,
        data_venda DATE,
        hash_pdf VARCHAR(64) UNIQUE
    )
    """)

    # Obter os hashes já cadastrados no banco para evitar duplicatas
    cursor.execute("SELECT hash_pdf FROM vendas")
    hashes_ja_existentes = {row[0] for row in cursor.fetchall()}

    # Processamento dos PDFs
    total_processados = 0
    total_ignorados = 0

    for arquivo in os.listdir(diretorio_pdf):
        if arquivo.endswith(".pdf"):
            total_processados += 1
            caminho_pdf = os.path.join(diretorio_pdf, arquivo)
            hash_pdf = gerar_hash_pdf(caminho_pdf)

            if hash_pdf in hashes_ja_existentes:
                total_ignorados += 1
                continue

            texto_contratos = extrair_texto_pdf(caminho_pdf)
            dados = extrair_dados_contrato(texto_contratos)

            # Validação dos dados extraídos
            if not dados["marca"] or not dados["modelo"] or not dados["ano"]:
                total_ignorados += 1
                print(f"Dados incompletos no PDF {arquivo}. Ignorando.")
                continue

            # Convertendo valores e validando
            try:
                valor_mensal = (
                    float(dados["valor_mensal"].replace(',', '.')) if dados["valor_mensal"] else None
                )
                duracao = int(dados["duracao"]) if dados["duracao"] else None

                query_insert = """
                    INSERT INTO vendas (marca, modelo, ano, cor, valor_mensal, duracao, data_venda, hash_pdf) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """

                valores = (
                    dados["marca"],
                    dados["modelo"],
                    int(dados["ano"]),
                    dados["cor"],
                    valor_mensal,
                    duracao,
                    pd.to_datetime('today').date(),
                    hash_pdf
                )

                cursor.execute(query_insert, valores)

            except ValueError as ve:
                print(f"Erro ao converter dados do PDF {arquivo}: {ve}")
            except pymysql.MySQLError as e:
                print(f"Erro ao inserir dados do PDF {arquivo}: {e}")

    # Ajustar o valor do AUTO_INCREMENT para o próximo ID correto
    cursor.execute("SELECT MAX(id) FROM vendas")
    max_id = cursor.fetchone()[0] or 0
    cursor.execute(f"ALTER TABLE vendas AUTO_INCREMENT = {max_id + 1}")

    print(f"Processo concluído. Total processados: {total_processados}, Total ignorados: {total_ignorados}")

except pymysql.MySQLError as err:
    print(f"Erro na conexão com o banco de dados: {err}")

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn.open:
        conn.close()
