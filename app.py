import streamlit as st
import pandas as pd
import sqlite3
from io import StringIO
import os
import math
from openai import OpenAI
import json
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1")


def sample_file_lines(file_content):
    lines = file_content.strip().split("\n")
    total = len(lines)

    if total <= 30:
        return "\n".join(lines)

    first_10 = lines[:10]
    middle_index = total // 2
    middle_10 = lines[middle_index-5:middle_index+5]
    last_10 = lines[-10:]

    sample = first_10 + middle_10 + last_10
    return "\n".join(sample)


def analyze_with_deepseek(sample_text):
    prompt = f"""
Analise a amostra do arquivo abaixo e retorne um JSON com:
- header_snake: lista dos nomes das colunas convertidos para snake_case
- delimiter: delimitador detectado (ex: ',', ';', '\\t')
- dtypes: lista com os tipos detectados (INTEGER, REAL, TEXT, DATE)
- sql_create_example: comando SQL para criar a tabela com base nos tipos detectados (use 'minha_tabela' como nome)
Responda apenas em JSON puro, sem comentários.
"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": sample_text}
        ],
        temperature=0
    )
    resposta = response.choices[0].message.content.strip()
    limpo = resposta.strip().removeprefix("```json").removesuffix("```").strip()
    print(limpo)
    return limpo


def create_table_sql(table_name, header_snake, dtypes):
    cols = [f"{col} {dtype}" for col, dtype in zip(header_snake, dtypes)]
    sql = f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(cols) + "\n);"
    return sql

st.set_page_config(page_title="ETL com DeepSeek")
st.subheader("Desafio Técnico | BU Sales & Marketing")
st.write("Este projeto em Python com Streamlit tem como objetivo demonstrar habilidades com upload e leitura de arquivos CSV ou TXT, aplicação de um processo ETL inteligente utilizando o modelo DeepSeek para pré-análise (detecção de cabeçalho em snake_case, delimitador e tipos de dados) e integração com banco de dados SQLite. O sistema separa as etapas de criação da tabela e inserção dos dados, exibindo também o SQL gerado para criação da estrutura no banco.")





uploaded_file = st.file_uploader("Escolha um arquivo CSV ou TXT", type=["csv", "txt"])

if uploaded_file:
    # Lê conteúdo bruto
    file_content = uploaded_file.getvalue().decode("utf-8", errors="ignore")
    sample_text = sample_file_lines(file_content)

    # Chama DeepSeek
    st.subheader("🤖 Analisando arquivo com DeepSeek...")
    deepseek_result = analyze_with_deepseek(sample_text)


    try:
        result_json = json.loads(deepseek_result)
        header_snake = result_json["header_snake"]
        delimiter = result_json["delimiter"]
        dtypes = result_json["dtypes"]
        sql_create_example = result_json.get("sql_create_example")
    except Exception as e:
        st.error(f"Erro ao interpretar resposta do DeepSeek: {e}")
        st.stop()

    st.write("**Cabeçalho (snake_case):**", header_snake)
    st.write("**Delimitador detectado:**", repr(delimiter))
    st.write("**Tipos detectados:**", dtypes)


    if delimiter.strip() == "" or delimiter.strip() == " ":

        df = pd.read_csv(
            StringIO(file_content),
            sep=r'\s{2,}',
            engine='python',
            skiprows=1,
            names=header_snake
        )
    else:

        df = pd.read_csv(
            StringIO(file_content),
            sep=delimiter,
            skiprows=1,
            names=header_snake,
            engine='python'
        )

    st.subheader("📊 DataFrame importado")
    st.dataframe(df.head())

    
    table_name = st.text_input("Nome da tabela no banco:", value="minha_tabela")
    sql_create = create_table_sql(table_name, header_snake, dtypes)
    st.subheader("📜 SQL de criação da tabela")
    st.code(sql_create, language="sql")


    if st.button("Criar tabela no banco (SQLite)"):
        conn = sqlite3.connect("meu_banco.db")
        cur = conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        cur.execute(sql_create)
        conn.commit()
        conn.close()
        st.success("Tabela criada com sucesso!")


    if st.button("Inserir dados no banco (SQLite)"):
        conn = sqlite3.connect("meu_banco.db")
        df.to_sql(table_name, conn, if_exists="append", index=False)
        conn.close()
        st.success(f"{len(df)} registros inseridos com sucesso!")
