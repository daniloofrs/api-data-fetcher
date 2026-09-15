# API Data Fetcher 🚀

Pipeline automatizado para extração, processamento e armazenamento de dados de câmbio de moedas (USD-BRL) em tempo real, utilizando Python, PostgreSQL e Docker.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Bibliotecas:** requests, psycopg (v3), python-dotenv
- **Banco de Dados:** PostgreSQL
- **Containerização:** Docker e Docker Compose
- **API Externa:** AwesomeAPI (Cotações de Moedas)

---

## 📋 Arquitetura e Funcionamento

1. O script consome os dados mais recentes da cotação USD-BRL via API REST.
2. Faz o parsing dos dados (taxa de compra e data/hora).
3. Salva uma cópia local estruturada em arquivo CSV na pasta /data.
4. Persiste os registros em uma tabela relacional (cotacoes) dentro do container PostgreSQL com persistência via volumes.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Docker e Docker Compose instalados.
- Git instalado.

### 1. Clonar o repositório
git clone https://github.com/daniloofrs/api-data-fetcher.git
cd api-data-fetcher

### 2. Configurar as variáveis de ambiente
Crie seu arquivo .env com base no .env.example:
cp .env.example .env

(Ajuste os valores no .env caso queira alterar a senha ou porta do banco)

### 3. Subir os containers com Docker Compose
docker compose up -d --build

### 4. Consultar os dados gravados no PostgreSQL
docker exec -it postgres-db psql -U postgres -d postgres -c "SELECT * FROM cotacoes;"

---

## 📁 Estrutura de Arquivos

├── data/                  # Diretório montado via volume com o CSV gerado
├── .dockerignore          # Arquivos ignorados pelo build do Docker
├── .env.example           # Modelo das variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo Git (.env, venv, etc.)
├── docker-compose.yml     # Orquestração dos containers (App + PostgreSQL)
├── Dockerfile             # Definição do container da aplicação Python
├── main.py                # Script principal do pipeline
└── requirements.txt       # Dependências do projeto