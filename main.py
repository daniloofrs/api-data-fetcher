import requests
import csv
import psycopg
from dotenv import load_dotenv
import os


def extrair_cotacoes():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    cotacoes = []
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
                dados = resposta.json()
                for item in dados.values():
                        moeda = f"{item['code']}-{item['codein']}"
                        valor = float(item['bid'])
                        data_hora = item['create_date']
                        cotacoes.append((moeda, valor, data_hora))
        else:
                print(
                    f"Erro na requisição: {resposta.status_code}"
                )
    except Exception as e:
         print(f"Erro na requisição: {e}")
    return cotacoes

cotacao = extrair_cotacoes()
for moeda,valor, data_hora in cotacao:
      print(moeda,valor,data_hora)


def salvar_no_banco(cotacoes):
    load_dotenv()
    cur = conn.cursor()


    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    conn = psycopg.connect(
        dbname = db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )

    cur.execute("SELECT 1 + 1;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cotacoes (
            id SERIAL PRIMARY KEY,
            moeda TEXT NOT NULL,
            valor NUMERIC(10, 4) NOT NULL,
            data_hora TIMESTAMP NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

      

