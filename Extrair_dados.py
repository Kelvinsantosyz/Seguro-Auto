import pandas as pd
import hashlib
import os
import pdfplumber
import re

# Função para extrair texto de um PDF
def extrair_texto_pdf(caminho_pdf):
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"
    return texto.strip()

# Função para extrair dados de contratos PDF
def extrair_dados_contrato(texto_contratos):
    texto_contratos = re.sub(r'\s+', ' ', texto_contratos).strip()

    padroes = {
        "marca": r"(?i)marca\s*[:\-]?\s*([a-zA-Z\s]+)",
        "modelo": r"(?i)modelo\s*[:\-]?\s*([a-zA-Z0-9\s]+)",
        "ano": r"(?i)ano\s*[:\-]?\s*(\d{4})",
        "cor": r"(?i)cor\s*[:\-]?\s*([A-Za-zÀ-ÿ\s]+)(?=,\s*placa|$)",  # Regex para capturar a cor
        "valor_mensal": r"(?i)valor mensal de\s*R\$\s*([\d,.]+)",
        "duracao": r"(?i)duração de\s*(\d+)\s*meses"
    }

    dados_extraidos = {}
    for chave, padrao in padroes.items():
        match = re.search(padrao, texto_contratos)
        if match:
            dados_extraidos[chave] = match.group(1).strip()  # Usar o primeiro grupo para pegar a informação
            print(f"Dados extraídos para {chave}: {dados_extraidos[chave]}")
        else:
            dados_extraidos[chave] = None
            print(f"Nenhum match encontrado para: {chave}")

    return dados_extraidos

# Função para gerar hash SHA256 do conteúdo do PDF
def gerar_hash_pdf(caminho_pdf):
    texto = extrair_texto_pdf(caminho_pdf)
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()

# Função principal para processar PDFs
def processar_pdfs(diretorio_pdf):
    resultados = []

    for arquivo in os.listdir(diretorio_pdf):
        if arquivo.endswith(".pdf"):
            caminho_pdf = os.path.join(diretorio_pdf, arquivo)
            hash_pdf = gerar_hash_pdf(caminho_pdf)

            # Extrair dados do contrato
            texto_contratos = extrair_texto_pdf(caminho_pdf)
            print(f"Texto extraído do PDF {arquivo}:\n{texto_contratos}\n")  # Imprimir o texto extraído
            dados = extrair_dados_contrato(texto_contratos)

            # Registro dos resultados
            resultado = {
                "arquivo": arquivo,
                "hash": hash_pdf,
                "marca": dados["marca"],
                "modelo": dados["modelo"],
                "ano": dados["ano"],
                "cor": dados["cor"],
                "valor_mensal": dados["valor_mensal"],
                "duracao": dados["duracao"]
            }
            resultados.append(resultado)

            # Validação de extração
            if not dados["marca"] or not dados["modelo"] or not dados["ano"]:
                print(f"Não foi possível extrair dados do PDF: {arquivo}")

    # Criar um DataFrame e salvar em um CSV
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(os.path.join(diretorio_pdf, 'resultados_extracao.csv'), index=False)

# Diretório onde estão os arquivos PDF
diretorio_pdf = r"C:\Users\Kelvin\Desktop\Projeto"

# Chamar a função principal
processar_pdfs(diretorio_pdf)
