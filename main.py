import requests
import csv
import psycopg
from dotenv import load_dotenv
import os

load_dotenv()


db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")


url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"

conn = psycopg.connect(
    dbname = db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)



cur = conn.cursor()

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



try:
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        cotacao = dados['USDBRL']
        print(f"Data: {cotacao['create_date']} | Valor do dólar: {cotacao['bid']}")
        cur.execute(
            "INSERT INTO cotacoes (moeda, valor, data_hora) VALUES (%s, %s, %s)",
            ("USD-BRL",float(cotacao['bid']), cotacao['create_date'])
        )

        conn.commit()
        print("Cotação gravada com sucesso!")

        with open('data/requisicoes.csv','a',newline='',encoding='utf-8-sig') as csvfile:
            delimitacao = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_ALL)
            delimitacao.writerow(['Cotação:'] + [cotacao['bid']] + ['Data: '] + [cotacao['create_date']])
    else:
        print(
            f"Erro na requisição: {resposta.status_code}"
        )

except requests.exceptions.RequestException as E:
    print(f"Erro ao falar com a API {E}")



finally:
    cur.close()
    conn.close()


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
                        data_hora = item(['create_date'])
                        cotacoes.append((moeda, valor, data_hora))
        else:
                print(
                    f"Erro na requisição: {resposta.status_code}"
                )
    except Exception as e:
         print(f"Erro na requisição: {e}")
    return cotacoes

