import requests
import csv
import psycopg
from dotenv import load_dotenv
import os
from pathlib import Path
import time
from datetime import datetime,timedelta



def extrair_cotacoes(data_extracao):
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
                        print(f"[INFO] [API] Cotação {moeda} obtida com sucesso: Valor: {valor} Data de extração: {data_extracao}")
        else:
                print(
                    f"Erro na requisição: {resposta.status_code}"
                )
    except Exception as e:
         print(f"Erro na requisição: {e}")
    return cotacoes

def salvar_no_banco(cotacoes, data_extracao):
    load_dotenv()

    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    with psycopg.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cotacoes (
                    id SERIAL PRIMARY KEY,
                    moeda TEXT NOT NULL,
                    valor NUMERIC(16, 4) NOT NULL,
                    data_hora TIMESTAMP NOT NULL,
                    data_extracao TIMESTAMP NOT NULL
                ); 
            """)

            for moeda, valor, data_hora in cotacoes:
                cur.execute(
                    """
                    INSERT INTO cotacoes (moeda, valor, data_hora, data_extracao)
                    VALUES (%s, %s, %s, %s);
                    """,
                    (moeda, valor, data_hora, data_extracao)
                )

        # Confirma a transação
        print("[INFO] [DB] 3 registros inseridos com sucesso na tabela 'cotacoes'.")
        conn.commit()

def salvar_no_csv(cotacoes, data_extracao):
    caminho = Path("data/requisicoes.csv")
    caminho.parent.mkdir(parents=True,exist_ok=True)
    arquivo_novo = not caminho.exists() or caminho.stat().st_size == 0
    with open(caminho, mode='a', newline='', encoding="utf-8") as f:
              escrever = csv.writer(f)

              if arquivo_novo:
                    escrever.writerow(["moeda","valor","data_hora", "data_extracao"])
              for moeda, valor, data_hora in cotacoes:
                    escrever.writerow([moeda, valor, data_hora, data_extracao])

    print("[INFO] [CSV] Dados anexados com sucesso em 'data/requisicoes.csv'.")
                


def main():
    data_extracao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cotacoes = extrair_cotacoes(data_extracao)
    if cotacoes:
          print("\n[INFO] [DB] Salvando no banco...")
          salvar_no_banco(cotacoes, data_extracao)
          time.sleep(2)
          print("[INFO] [CSV] Salvando no CSV...\n")
          salvar_no_csv(cotacoes, data_extracao)
    else:
          print("Nenhuma cotação foi extraída.")

if __name__ == "__main__":
      minutos_espera = 15
      usuario = 'Danilo'


      print(f"USUÁRIO: {usuario.capitalize()}\n[INFO] [INIT] Coletor iniciado. Intervalo de execução: {minutos_espera} minutos.\n")
      time.sleep(0.5)
      while True:
            proxima_coleta = datetime.now() + timedelta(minutes=minutos_espera)
            print("[INFO] [START] Iniciando ciclo de extração das cotações...\n")
            try:
                time.sleep(1)
                main()
                print("[INFO] [DONE] Ciclo concluído com sucesso.")
                time.sleep(0.5)
            except Exception as e:
                  print(f"Ocorreu um erro na requisição: {e}")
            print("\n ---------------------------------------------------")
            print(f"\n[INFO] Próxima requisição agendada para: {proxima_coleta.strftime('%H:%M')} ")
            time.sleep(1)


            print(f"[PAUSA] Olá {usuario.capitalize()}, Faltam 15 minutos para a próxima requisição.")
            time.sleep(60 * 5)
            print(f"[PAUSA] Olá {usuario.capitalize()}, Faltam 10 minutos para a próxima requisição.")
            time.sleep(60 * 5)
            print(f"[PAUSA] Olá {usuario.capitalize()}, Faltam 5 minutos para a próxima requisição.")
            time.sleep(60 * 4)
            print(f"[PAUSA] Olá {usuario.capitalize()}, Faltaz 1 minuto para a próxima requisição.")
            time.sleep(60 * 1)


      