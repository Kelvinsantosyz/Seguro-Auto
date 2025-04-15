import pymysql
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, 
    QVBoxLayout, QPushButton, QWidget, QTabWidget, QHeaderView
)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score
import locale

# Configuração regional para moeda em português
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Função para obter a inflação
def obter_inflacao():
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = 'https://www.bcb.gov.br'
    driver.get(url)
    try:
        div_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.percentual.light.mr-2'))
        )
        percentual = div_element.text.strip()
        if not percentual:
            print("Erro: Taxa de inflação não encontrada na página.")
            driver.quit()
            return None
        percentual = percentual.replace(',', '.').replace('%', '')
        taxa_inflacao = float(percentual) / 100
        print(f'Taxa de Inflação obtida: {taxa_inflacao * 100}%')
        driver.quit()
        return taxa_inflacao
    except Exception as e:
        print(f'Ocorreu um erro ao obter a taxa de inflação: {e}')
        driver.quit()
        return None

# Função para conectar ao banco de dados MySQL
def conectar_banco():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="305614",
            database="seu_banco_de_dados",
            autocommit=True
        )
        print("Conexão bem-sucedida ao banco de dados!")
        return conn
    except pymysql.MySQLError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para buscar dados no banco de dados
def buscar_dados():
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT marca, modelo, ano, valor_mensal, COUNT(*) as quantidade_contratos FROM vendas GROUP BY marca, modelo, ano, valor_mensal")
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    else:
        return []

# Função para ajustar os preços com base na inflação e outros fatores
def ajustar_precos(df, taxa_inflacao):
    df['Valor_Mensal'] = pd.to_numeric(df['Valor_Mensal'], errors='coerce')
    df['Quantidade_Contratos'] = pd.to_numeric(df['Quantidade_Contratos'], errors='coerce')
    df = df.dropna(subset=['Valor_Mensal', 'Quantidade_Contratos'])
    if df.empty:
        print("Erro: Não há dados válidos após limpeza.")
        return df

    risco_ano = df['Ano'].apply(lambda x: 1.1 if x < 2015 else 1.05)
    risco_quantidade = df['Quantidade_Contratos'].apply(lambda x: 1.05 if x > df['Quantidade_Contratos'].mean() else 0.95)
    risco_inflacao = 1 + taxa_inflacao

    df['Novo valor mensal 2025'] = df['Valor_Mensal'] * risco_ano * risco_quantidade * risco_inflacao

    X = df[['Quantidade_Contratos', 'Ano']]
    y = df['Valor_Mensal']
    modelo = LinearRegression()

    scores = cross_val_score(modelo, X, y, cv=5, scoring='neg_mean_squared_error')
    mse_medio = -np.mean(scores)
    print(f'Média do erro quadrático médio (MSE) após validação cruzada: {mse_medio:.2f}')
    modelo.fit(X, y)
    r2 = r2_score(y, modelo.predict(X))
    print(f'R² do modelo: {r2:.2f}')

    df['Valor Previsto 2026'] = modelo.predict(X)
    df['Percentual_Aumento'] = ((df['Novo valor mensal 2025'] - df['Valor_Mensal']) / df['Valor_Mensal']) * 100
    df['Houve_Diminuicao'] = df['Percentual_Aumento'].apply(lambda x: 'Sim' if x < 0 else 'Não')

    # Verificação se o valor previsto para 2026 diminuiu
    df['Diminuiu_2026'] = df.apply(
        lambda row: f"Sim ({((row['Valor_Mensal'] - row['Valor Previsto 2026']) / row['Valor_Mensal']) * 100:.2f}%)" 
        if row['Valor Previsto 2026'] < row['Valor_Mensal'] else 'Não', 
        axis=1
    )

    return df

# Interface gráfica com PyQt5
class MainWindow(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Ajuste de Preços de Seguros de Veículos")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #f5f5f5; color: #333; font-family: Arial, sans-serif;")
        
        layout_principal = QVBoxLayout()
        abas = QTabWidget()

        # Aba 1 - Resumo de Valores
        aba_tabela = QWidget()
        layout1 = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, row in df.iterrows():
            for j, val in enumerate(row):
                col_name = df.columns[j]
                if col_name not in ['Ano', 'Quantidade_Contratos']:
                    if isinstance(val, (float, int)):
                        if "Percentual" in col_name:
                            val = f"{val:.2f}%"
                        else:
                            val = locale.currency(val, grouping=True)
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        layout1.addWidget(self.tableWidget)

        fig, ax = plt.subplots(figsize=(14, 7))
        indices = np.arange(len(df))
        ax.bar(indices - 0.2, df['Valor_Mensal'], width=0.4, label='Valor Original', color='#3498db', edgecolor='black', linewidth=1.5)
        ax.bar(indices + 0.2, df['Novo valor mensal 2025'], width=0.4, label='Novo Valor', color='#e74c3c', edgecolor='black', linewidth=1.5)
        ax.set_xticks(indices)
        ax.set_xticklabels([f"{row['Marca']}\n{row['Modelo']}" for _, row in df.iterrows()], rotation=45, ha='right', fontsize=10)
        ax.set_xlabel('Veículo', fontsize=12, fontweight='bold')
        ax.set_ylabel('Valor Mensal (R$)', fontsize=12, fontweight='bold')
        ax.set_title('Comparativo de Valores: Original vs Novo', fontsize=14, fontweight='bold')
        ax.legend(fontsize=12, loc='upper left')
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        canvas = FigureCanvas(fig)
        layout1.addWidget(canvas)
        canvas.draw()

        btn_fechar = QPushButton("Fechar")
        btn_fechar.setStyleSheet("background-color: #e74c3c; color: #fff; padding: 10px; font-size: 14px; border-radius: 5px;")
        btn_fechar.clicked.connect(self.close)
        layout1.addWidget(btn_fechar)

        aba_tabela.setLayout(layout1)

        # Aba 2 - Percentual de Aumento
        aba_percentual = QWidget()
        layout2 = QVBoxLayout()
        tabela_percentual = QTableWidget()
        tabela_percentual.setRowCount(len(df))
        tabela_percentual.setColumnCount(6)
        tabela_percentual.setHorizontalHeaderLabels([
            'Marca', 'Modelo', 'Ano', 
            'Percentual de Aumento', 
            'Houve Diminuição (2025)', 
            'Diminuiu em 2026'
        ])

        for i, row in df.iterrows():
            tabela_percentual.setItem(i, 0, QTableWidgetItem(str(row['Marca'])))
            tabela_percentual.setItem(i, 1, QTableWidgetItem(str(row['Modelo'])))
            tabela_percentual.setItem(i, 2, QTableWidgetItem(str(row['Ano'])))
            tabela_percentual.setItem(i, 3, QTableWidgetItem(f"{row['Percentual_Aumento']:.2f}%"))
            tabela_percentual.setItem(i, 4, QTableWidgetItem(str(row['Houve_Diminuicao'])))
            tabela_percentual.setItem(i, 5, QTableWidgetItem(str(row['Diminuiu_2026'])))

        layout2.addWidget(tabela_percentual)
        aba_percentual.setLayout(layout2)

        # Aba 3 - Valor Previsto para 2026
        aba_grafico_2026 = QWidget()
        layout3 = QVBoxLayout()
        fig2, ax2 = plt.subplots(figsize=(14, 7))
        indices2 = np.arange(len(df))
        ax2.bar(indices2, df['Valor Previsto 2026'], color='#2ecc71', edgecolor='black', linewidth=1.5)
        ax2.set_xticks(indices2)
        ax2.set_xticklabels([f"{row['Marca']}\n{row['Modelo']}" for _, row in df.iterrows()], rotation=45, ha='right', fontsize=10)
        ax2.set_xlabel('Veículo', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Valor Previsto (R$)', fontsize=12, fontweight='bold')
        ax2.set_title('Valor Previsto para 2026', fontsize=14, fontweight='bold')
        ax2.grid(axis='y', linestyle='--', alpha=0.7)

        canvas2 = FigureCanvas(fig2)
        layout3.addWidget(canvas2)
        canvas2.draw()

        aba_grafico_2026.setLayout(layout3)

        # Adiciona abas ao widget
        abas.addTab(aba_tabela, "Resumo de Valores")
        abas.addTab(aba_percentual, "Percentual de Aumento")
        abas.addTab(aba_grafico_2026, "Valor Previsto para 2026")

        layout_principal.addWidget(abas)
        container = QWidget()
        container.setLayout(layout_principal)
        self.setCentralWidget(container)

# Execução do programa
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dados = buscar_dados()
    if dados:
        df = pd.DataFrame(dados, columns=['Marca', 'Modelo', 'Ano', 'Valor_Mensal', 'Quantidade_Contratos'])
        taxa_inflacao = obter_inflacao()
        if taxa_inflacao is not None:
            df = ajustar_precos(df, taxa_inflacao)
            window = MainWindow(df)
            window.show()
            sys.exit(app.exec_())
        else:
            print("Não foi possível obter a taxa de inflação.")
    else:
        print("Nenhum dado encontrado no banco de dados.")
