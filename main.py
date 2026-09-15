import requests
import csv
import psycopg
from dotenv import load_dotenv
import os
from pathlib import Path


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

def salvar_no_banco(cotacoes):



    load_dotenv() #Pega as chaves do .env



    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    # Atribui valores as chaves que eu peguei.


    conn = psycopg.connect(
        dbname = db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    #Conecta com o postgres

    cur = conn.cursor() #Envia o comando.
    cur.execute("SELECT 1 + 1;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cotacoes (
            id SERIAL PRIMARY KEY,
            moeda TEXT NOT NULL,
            valor NUMERIC(16, 4) NOT NULL,
            data_hora TIMESTAMP NOT NULL
        ); 
    """)
    conn.commit() #Comita o que eu executo.


    for moeda, valor, data_hora in cotacoes:
          cur.execute(
                "INSERT INTO cotacoes (moeda, valor, data_hora) VALUES (%s, %s, %s)",
                (moeda, valor, data_hora)
                
          )
    conn.commit()



    cur.close()
    conn.close()

def salvar_no_csv(cotacoes):
    caminho = Path("data/requisicoes.csv")
    caminho.parent.mkdir(parents=True,exist_ok=True)
    arquivo_novo = not caminho.exists() or caminho.stat().st_size == 0
    with open(caminho, mode='a', newline='', encoding="utf-8") as f:
              escrever = csv.writer(f)

              if arquivo_novo:
                    escrever.writerow(["moeda","valor","data_hora"])
              for moeda, valor, data_hora in cotacoes:
                    escrever.writerow([moeda, valor, data_hora])
                    print(f"Sucesso: {moeda, valor, data_hora}")
                


def main():
    cotacoes = extrair_cotacoes()
    if cotacoes:
          salvar_no_banco(cotacoes)
          salvar_no_csv(cotacoes)
    else:
          print("Nenhuma cotação foi extraída.")

if __name__ == "__main__":
      main()
      