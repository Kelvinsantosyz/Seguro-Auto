
-----

# 🚗 Analitica Seguro Auto: Otimização de Precificação com Inteligência de Dados

-----

## 📄 Introdução

Bem-vindos ao projeto **Analitica Seguro Auto**, desenvolvido para a disciplina de **PROJETO EM SISTEMAS INTELIGENTES** da Universidade Nove de Julho (UNINOVE), sob a orientação do Prof. Dr. Edson Melo de Souza.

No dinâmico mercado de seguros automotivos, a **precificação assertiva** e **personalizada** é um diferencial competitivo crucial. Este projeto aborda o desafio de otimizar essa precificação, utilizando o poder da análise de dados e do aprendizado de máquina. Nosso objetivo é desenvolver um sistema que não apenas prevê riscos de sinistros com maior precisão, mas também facilita a visualização e a interação com esses dados para as seguradoras.

-----

## ✨ Recursos e Funcionalidades

O sistema **Analitica Seguro Auto** oferece uma série de funcionalidades que visam revolucionar a forma como as seguradoras precificam suas apólices:

  * **Extração de Dados Robustos:** Capacidade de coletar informações de diversas fontes, incluindo documentos PDF e websites.
  * **Modelagem Preditiva Avançada:** Utilização de algoritmos de **Machine Learning** para prever a probabilidade de sinistros e auxiliar na definição do prêmio.
  * **Interface Gráfica Intuitiva:** Um painel interativo que permite aos usuários inserir dados, visualizar análises e interpretar os resultados de forma clara.
  * **Integração com Banco de Dados:** Armazenamento seguro e eficiente de todas as informações processadas e modelos gerados.
  * **Visualização de Dados:** Gráficos e tabelas dinâmicas que facilitam a compreensão dos padrões e tendências nos dados de risco.

-----

## 🛠️ Tecnologias Utilizadas

Para construir o **Analitica Seguro Auto**, empregamos um conjunto robusto de bibliotecas e ferramentas Python, cada uma com um papel específico:

### 📦 Visão Geral das Bibliotecas

| Biblioteca | Principal Uso |
| :--------- | :------------ |
| `pymysql` | Conexão e manipulação de banco de dados MySQL |
| `pandas` | Manipulação, limpeza e análise de dados (DataFrames) |
| `numpy` | Cálculos numéricos e operações com arrays |
| `scikit-learn` | Construção de modelos de Regressão linear e avaliação de modelos |
| `matplotlib` | Criação de gráficos e visualizações de dados |
| `PyQt5` | Desenvolvimento da interface gráfica do usuário |
| `selenium` | Web scraping e automação de navegação web |
| `webdriver-manager` | Gerenciamento automático de drivers de navegador |
| `pdfplumber` | Extração de texto e tabelas de arquivos PDF |
| `re` | Processamento e filtragem de texto com expressões regulares |
| `hashlib` | Geração de hashes para garantir a integridade de PDFs |
| `locale` | Configuração de formatos locais para números e datas |
| `os` | Interação com o sistema operacional (arquivos e diretórios) |

### 🧠 Detalhamento das Funções Chave

  * **Extração de Dados de PDF (`pdfplumber`, `re`, `hashlib`):**

      * **`pdfplumber`**: Precisão na extração de texto, tabelas e estruturas de parágrafos de PDFs.
      * **`re`**: Essencial para limpar e padronizar as informações extraídas através de expressões regulares.
      * **`hashlib`**: Garante a integridade e identificação única dos documentos PDF processados.

  * **Machine Learning e Estatística (`scikit-learn`, `numpy`):**

      * **`scikit-learn` (`sklearn`)**: A base dos nossos modelos preditivos.
          * `LinearRegression`: Utilizada para criar os modelos de regressão linear para previsão.
          * `cross_val_score`: Garante a robustez do modelo através de validação cruzada.
          * `r2_score`: Métrica chave para avaliar a performance e a qualidade do nosso modelo preditivo.
      * **`numpy`**: Fornece as ferramentas para cálculos numéricos eficientes, fundamentais para operações de machine learning.

  * **Visualização de Dados (`matplotlib`, `matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg`):**

      * **`matplotlib`**: A biblioteca principal para criar visualizações claras e informativas dos dados.
      * **`FigureCanvasQTAgg`**: Permite integrar perfeitamente os gráficos do Matplotlib dentro da nossa interface gráfica desenvolvida com PyQt5.

  * **Interface Gráfica (`PyQt5`):**

      * **`PyQt5`**: O framework escolhido para desenvolver a interface de usuário interativa e amigável, crucial para a usabilidade do sistema.

  * **Automação de Navegador (`selenium`, `webdriver_manager`):**

      * **`selenium`**: A ferramenta poderosa para automatizar a navegação em sites, permitindo o web scraping e a interação com páginas web para coleta de dados. Usamos `webdriver`, `By`, `WebDriverWait`, `expected_conditions` para controle preciso.
      * **`webdriver_manager`**: Simplifica a gestão e instalação dos drivers necessários para o Selenium, garantindo compatibilidade e facilidade de configuração.

  * **Banco de Dados (`pymysql`):**

      * **`pymysql`**: Facilita a conexão direta e a manipulação dos dados no banco de dados MySQL, garantindo persistência e organização das informações.

  * **Outras (`locale`, `os`, `pandas`):**

      * **`locale`**: Utilizado para configurar o formato local de exibição de números e datas, importante para padronização.
      * **`os`**: Módulo padrão para interagir com o sistema operacional, auxiliando na manipulação de arquivos e diretórios.
      * **`pandas`**: Indispensável para a organização, limpeza e transformação de dados em tabelas (DataFrames), preparando-os para a análise e modelagem.

-----

## 🚀 Como Executar o Projeto

Para colocar o **Analitica Seguro Auto** para rodar em sua máquina, siga estes passos simples:

1.  **Pré-requisitos:** Certifique-se de ter o **Python 3.x** instalado.
2.  **Instale todas as bibliotecas necessárias** utilizando o comando abaixo no seu terminal:
    ```bash
    pip install pymysql pandas numpy scikit-learn matplotlib pyqt5 selenium webdriver-manager pdfplumber
    ```
3.  **Clone o repositório** (se aplicável, adicione instruções para clonar o repositório do GitHub aqui).
4.  **Execute o script principal** (adicione aqui o comando para rodar o script, ex: `python main.py`).

-----

## 📸 Demonstração do Projeto

Confira algumas capturas de tela da nossa aplicação em funcionamento:

[Download do vídeo de demonstração](https://www.google.com/search?q=./compressed_video_25mb.mp4)

-----

## 👨‍💻 Equipe de Desenvolvimento

Este projeto foi desenvolvido com dedicação pela seguinte equipe:

  * **Kelvin**: Gerente de Projeto, Engenheiro de Dados e UI/UX Designer
  * **Thiago**: Cientista de Dados
  * **Miguel**: Geração de Documentação

-----

## 📚 Referências

  * DORNELAS, J. C. A. **Empreendedorismo: Transformando Ideias em Negócios**. 6. ed. Rio de Janeiro: LTC, 2015.
  * SEVERINO, A. J. **Metodologia do Trabalho Científico**. 22. ed. São Paulo: Cortez, 2002.

### Documentação das Ferramentas e Bibliotecas Utilizadas

  * **Banco Central do Brasil (BCB)**. Disponível em: [https://www.bcb.gov.br](https://www.bcb.gov.br). Acesso em: 31 mai. 2025.
  * **hashlib**. Disponível em: [https://docs.python.org/3/library/hashlib.html](https://docs.python.org/3/library/hashlib.html). Acesso em: 31 mai. 2025.
  * **locale**. Disponível em: [https://docs.python.org/3/library/locale.html](https://docs.python.org/3/library/locale.html). Acesso em: 31 mai. 2025.
  * **matplotlib**. Disponível em: [https://matplotlib.org/stable/contents.html](https://matplotlib.org/stable/contents.html). Acesso em: 31 mai. 2025.
  * **numpy**. Disponível em: [https://numpy.org/doc/](https://numpy.org/doc/). Acesso em: 31 mai. 2025.
  * **os**. Disponível em: [https://docs.python.org/3/library/os.html](https://docs.python.org/3/library/os.html). Acesso em: 31 mai. 2025.
  * **pandas**. Disponível em: [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/). Acesso em: 31 mai. 2025.
  * **pdfplumber**. Disponível em: [https://github.com/jsvine/pdfplumber](https://github.com/jsvine/pdfplumber). Acesso em: 31 mai. 2025.
  * **PyQt5**. Disponível em: [https://doc.qt.io/qtforpython/PyQt5/](https://www.google.com/search?q=https://doc.qt.io/qtforpython/PyQt5/). Acesso em: 31 mai. 2025.
  * **pymysql**. Disponível em: [https://pymysql.readthedocs.io/en/latest/](https://pymysql.readthedocs.io/en/latest/). Acesso em: 31 mai. 2025.
  * **re**. Disponível em: [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html). Acesso em: 31 mai. 2025.
  * **scikit-learn (sklearn)**. Disponível em: [https://scikit-learn.org/stable/documentation.html](https://scikit-learn.org/stable/documentation.html). Acesso em: 31 mai. 2025.
  * **selenium**. Disponível em: [https://www.selenium.dev/documentation/](https://www.selenium.dev/documentation/). Acesso em: 31 mai. 2025.
  * **webdriver-manager**. Disponível em: [https://pypi.org/project/webdriver-manager/](https://pypi.org/project/webdriver-manager/). Acesso em: 31 mai. 2025.

-----
