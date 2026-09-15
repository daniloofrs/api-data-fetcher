import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


conn = psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)


cur = conn.cursor()


cur.execute("""
    SELECT
        COUNT(*) AS total_registros,
        MIN(valor) AS cotacao_minima,
        MAX(valor) AS cotacao_maxima,
        ROUND(AVG(valor), 4) AS media_cotacao,
        COALESCE(ROUND(STDDEV(valor), 4), 0) AS desvio_padrao
    FROM cotacoes;
""")

resultado = cur.fetchone()


print("--- Resumo das Cotações Acumuladas ---")
print(f"Total de registros: {resultado[0]}")
print(f"Mínima:             R$ {resultado[1]}")
print(f"Máxima:             R$ {resultado[2]}")
print(f"Média:              R$ {resultado[3]}")
print(f"Volatilidade (Std): R$ {resultado[4]}")

cur.close()
conn.close()