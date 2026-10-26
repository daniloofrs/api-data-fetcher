# API Data Fetcher

[![CI](https://github.com/daniloofrs/api-data-fetcher/actions/workflows/ci.yml/badge.svg)](https://github.com/daniloofrs/api-data-fetcher/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)


Aqui você encontra uma aplicação em Python que consulta as cotações de moedas (USD, EUR e BTC para BRL) a cada 15 minutos e grava o histórico tanto no PostgreSQL quanto num arquivo CSV.

### Demonstração

<p align="center">
  <img width="700" alt="Demonstração do pipeline em execução" src="https://github.com/user-attachments/assets/206d890e-96f5-4c5d-bf01-7d061d25d395" />
</p>

<p align="center">
  <sub>Fluxo da aplicação: consulta à API, gravação no banco e histórico salvo num CSV local.</sub>
</p>

### Logs da coleta
Seu terminal mostra cada requisição feita, a confirmação do banco e uma contagem regressiva até a próxima rodada:

<img width="400" alt="Logs de Execução e Agendamento do Pipeline" src="https://github.com/user-attachments/assets/43383327-af0a-4f75-a75d-75b3c96ed44a" />

---

### Histórico acumulado em CSV
Dá pra ver como os dados vão se acumulando linha a linha no seu arquivo `data/requisicoes.csv`:

<img width="400" alt="Histórico Acumulado no Arquivo CSV" src="https://github.com/user-attachments/assets/b6635d55-7eae-470f-b881-4a80f350696a" />

---

### Containers em execução
Aqui você confere os containers da sua aplicação e do PostgreSQL rodando juntos via Docker Compose:

<img width="400" alt="Containers Docker e Docker Compose UP" src="https://github.com/user-attachments/assets/5b478079-b9a2-4561-a360-34025a15f744" />

---

## O que usamos aqui

- Python 3.12 (funciona bem a partir do 3.11)
- PostgreSQL
- Docker e Docker Compose
- Bibliotecas: `requests`, `psycopg` (v3) e `python-dotenv`
- [AwesomeAPI](https://docs.awesomeapi.com.br/) pras cotações em tempo real

---

## Como funciona por baixo dos panos

1. O script faz chamadas na AwesomeAPI buscando as cotações atuais de USD-BRL, EUR-BRL e BTC-BRL.
2. Pega o preço de compra (`valor`), o horário retornado e marca a data exata da sua extração.
3. Conecta no PostgreSQL e insere tudo na tabela `cotacoes` (seus dados ficam salvos num volume do Docker).
4. Grava uma cópia incremental no final do seu arquivo `data/requisicoes.csv`.
5. Fica em pausa no terminal e repete esse ciclo a cada 15 minutos.

---

## Como rodar na sua máquina

### O que você precisa antes
- Docker e Docker Compose instalados no seu computador.
- Git pra clonar o repositório.

### 1. Clone o repositório
```bash
git clone https://github.com/daniloofrs/api-data-fetcher.git
cd api-data-fetcher
```

### 2. Prepare suas variáveis de ambiente
Crie o seu `.env` copiando nosso arquivo de exemplo:
```bash
cp .env.example .env
```
Se você quiser alterar a senha, porta ou usuário do seu banco, é só editar esse arquivo antes de subir tudo.

### 3. Suba os containers
```bash
docker compose up -d --build
```

### 4. Veja seus logs em tempo real
Pra você acompanhar o coletor em ação:
```bash
docker logs -f api-fetcher-app
```

### 5. Consulte seus dados no PostgreSQL
Pra conferir se tá tudo salvo no banco, você pode entrar direto no container do Postgres:
```bash
docker exec -it postgres-db psql -U postgres -d postgres -c "SELECT * FROM cotacoes ORDER BY id DESC LIMIT 10;"
```
Caso você tenha trocado o `DB_USER` ou `DB_NAME` no seu `.env`, ajuste os parâmetros `-U` e `-d` pro seu caso.

### 6. Rode a análise estatística
Deixamos um script pronto (`analytics.py`) pra você ver média, mínima, máxima e volatilidade das cotações. Dá pra rodar direto no container:

```bash
docker exec -it api-fetcher-app python analytics.py
```
Ou rodar na sua máquina com Python local: `python analytics.py`.

---

## Estrutura do projeto

```text
api-data-fetcher/
├── data/                  # CSV gerado pelo pipeline (volume compartilhado)
├── .dockerignore          # O que não vai pro build do Docker
├── .env.example           # Modelo pras suas variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo Git
├── analytics.py           # Script pra puxar métricas do seu banco
├── docker-compose.yml     # Orquestração dos containers
├── Dockerfile             # Imagem da aplicação Python
├── main.py                # Script do coletor
└── requirements.txt       # Dependências Python
```
