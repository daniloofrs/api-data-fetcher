import requests
import csv
import psycopg

url = "https://economia.awesomeapi.com.br/last/USD-BRL"
conn = psycopg.connect("dbname=postgres user=postgres password=senha host=localhost port=5432")

try:
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        cotacao = dados['USDBRL']
        print(f"Data: {cotacao['create_date']} | Valor do dólar: {cotacao['bid']}")

        with open('data/requisicoes.csv','w',newline='',encoding='utf-8-sig') as csvfile:
            delimitacao = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_ALL)
            delimitacao.writerow(['Cotação:'] + [cotacao['bid']] + ['Data: '] + [cotacao['create_date']])
    else:
        print(
            f"Erro na requisição: {resposta.status_code}"
        )

except requests.exceptions.RequestException as E:
    print(f"Erro ao falar com a API {E}")