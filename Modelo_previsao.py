import pymysql
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import locale
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configurar locale para exibição em formato de moeda brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Função para obter a inflação do site do Banco Central
def obter_inflacao():
    # Configuração do driver do Selenium (Chrome)
    options = webdriver.ChromeOptions()
    options.headless = True  # Modo sem interface do navegador

    # Inicializando o WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Acessando o site
    url = 'https://www.bcb.gov.br'
    driver.get(url)

    try:
        # Espera explícita até que o elemento com a inflação esteja visível
        div_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.percentual.light.mr-2'))
        )

        # Extrair o valor da inflação
        percentual = div_element.text.strip()

        # Fechar o navegador após a execução
        driver.quit()

        # Remover o símbolo '%' e substituir vírgula por ponto
        percentual = percentual.replace(',', '.').replace('%', '')

        # Tentar converter para float
        taxa_inflacao = float(percentual) / 100
        
        # Exibir o valor da inflação
        print(f'Taxa de Inflação obtida: {taxa_inflacao * 100}%')
        return taxa_inflacao
    
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
        driver.quit()
        return None

# Função para conectar ao banco de dados MySQL
def conectar_banco():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="305614",  # Substitua pela sua senha do MySQL
        database="seu_banco_de_dados",  # Substitua pelo nome do seu banco de dados
        autocommit=True
    )

# Função para buscar os dados no banco
def buscar_dados():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT marca, modelo, ano, valor_mensal, COUNT(*) as quantidade_contratos FROM vendas GROUP BY marca, modelo, ano, valor_mensal")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# Função para ajustar os preços com base na demanda e inflação
def ajustar_precos(df, taxa_inflacao):
    # Modelo de Regressão Linear
    X = df[['Quantidade_Contratos']]
    y = df['Valor_Mensal']
    modelo = LinearRegression()
    modelo.fit(X, y)
    df['Valor_Previsto'] = modelo.predict(X)

    # Ajuste dinâmico de preços baseado na inflação e na demanda
    df['Novo_Valor_Mensal'] = np.where(
        df['Quantidade_Contratos'] > df['Quantidade_Contratos'].mean(),
        df['Valor_Mensal'] * 1.036 * (1 + taxa_inflacao),  # Aumento por demanda e inflação
        df['Valor_Mensal'] * 0.95 * (1 + taxa_inflacao)  # Redução por baixa demanda e inflação
    )
    
    # Imprimir os valores originais e ajustados formatados como moeda
    print("\nValores de 'Valor_Mensal' (Original) e 'Novo_Valor_Mensal' (Ajustado):")
    for i, row in df.iterrows():
        valor_original = locale.currency(row['Valor_Mensal'], grouping=True)
        novo_valor = locale.currency(row['Novo_Valor_Mensal'], grouping=True)
        print(f"{row['Marca']} {row['Modelo']} ({row['Ano']}): Valor Original = {valor_original}, Novo Valor = {novo_valor}")
    
    return df

# Função para criar interface gráfica
def exibir_interface(df):
    janela = tk.Tk()
    janela.title('Ajuste de Preços de Seguros de Veículos')
    janela.geometry('800x400')

    # Tabela com os dados
    colunas = list(df.columns)
    tabela = ttk.Treeview(janela, columns=colunas, show='headings')
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=100)

    for _, row in df.iterrows():
        tabela.insert('', 'end', values=list(row))
    tabela.pack(fill='both', expand=True)

    # Gráfico interativo
    fig, ax = plt.subplots()
    ax.plot(df['Quantidade_Contratos'], df['Valor_Mensal'], label='Valor Original', marker='o')
    ax.plot(df['Quantidade_Contratos'], df['Novo_Valor_Mensal'], label='Novo Valor', marker='x')
    ax.set_xlabel('Quantidade de Contratos')
    ax.set_ylabel('Valor Mensal (R$)')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.get_tk_widget().pack()
    canvas.draw()

    janela.mainloop()

# Execução do fluxo
dados = buscar_dados()
if dados:
    df = pd.DataFrame(dados, columns=['Marca', 'Modelo', 'Ano', 'Valor_Mensal', 'Quantidade_Contratos'])

    # Obter a taxa de inflação atualizada
    taxa_inflacao = obter_inflacao()

    if taxa_inflacao is not None:
        # Ajustar preços com base na demanda e inflação
        df = ajustar_precos(df, taxa_inflacao)

        # Exibir a interface gráfica com a tabela e gráfico
        exibir_interface(df)
    else:
        print("Não foi possível obter a taxa de inflação.")
else:
    print("Nenhum dado encontrado no banco de dados.")
