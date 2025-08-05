# 🚀 Desafio Técnico | BU Sales & Marketing

# ETL Inteligente com DeepSeek e Streamlit

## 📌 Descrição
Este projeto implementa um pipeline **ETL** (Extract, Transform, Load) utilizando **Python** e **Streamlit** para interface web.  
O objetivo é processar arquivos CSV ou TXT, realizar uma pré-análise automatizada com o modelo **DeepSeek** e integrar os dados a um banco de dados **SQLite**.

---

## 🚀 Funcionalidades
- **Upload de arquivos** nos formatos `.csv` e `.txt`.
- **Amostragem inteligente**: envio de 10 linhas iniciais, 10 do meio e 10 finais (ou arquivo completo se tiver < 30 linhas) para análise.
- **Análise com DeepSeek** para:
  - Conversão dos nomes de colunas para `snake_case`.
  - Detecção do delimitador.
  - Inferência dos tipos de dados (`INTEGER`, `REAL`, `TEXT`, `DATE`).
  - Geração de SQL `CREATE TABLE`.
- **Importação ajustada**:
  - Pula sempre a primeira linha (`skiprows=1`).
- **Banco de dados SQLite**:
  - Criação da tabela de forma separada.
  - Inserção de dados controlada.
- **Visualização dos dados** no `pandas.DataFrame`.

---

## 🛠 Tecnologias Utilizadas
- [Python 3.11+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [SQLite3](https://www.sqlite.org/index.html)
- [DeepSeek API](https://www.deepseek.com/)

---

## 📂 Estrutura do Projeto
```
etl_deepseek/
│── app.py              # Aplicação principal em Streamlit
│── requirements.txt    # Dependências do projeto
│── README.md           # Documentação do projeto
```