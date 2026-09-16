# API Data Fetcher

Pipeline automatizado para extração, processamento e armazenamento de dados de câmbio de moedas (USD-BRL) em tempo real, utilizando Python, PostgreSQL e Docker.

## 📸 Demonstração e Evidências de Execução

Abaixo estão as evidências do funcionamento contínuo, persistência e isolamento do pipeline.

### 1. Logs da Aplicação em Tempo Real
Registro da extração das cotações (USD, EUR e BTC), persistência relacional no banco de dados, gravação em disco e gerenciamento dos ciclos de agendamento:

<img width="1110" height="851" alt="codigo" src="https://github.com/user-attachments/assets/43383327-af0a-4f75-a75d-75b3c96ed44a" />

---

### 2. Persistência Incremental em CSV
Histórico cronológico acumulado no arquivo `data/requisicoes.csv`, demonstrando a ingestão contínua a cada intervalo programado:

<img width="507" height="848" alt="csv" src="https://github.com/user-attachments/assets/b6635d55-7eae-470f-b881-4a80f350696a" />

---

### 3. Orquestração e Ambiente com Docker
Containers da aplicação e do PostgreSQL operando em segundo plano via Docker Compose com portas e volumes devidamente mapeados:

<img width="811" height="379" alt="docker" src="https://github.com/user-attachments/assets/5b478079-b9a2-4561-a360-34025a15f744" />

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

```text
api-data-fetcher/
├── data/                  # Diretório montado via volume com o CSV gerado
├── .dockerignore          # Arquivos ignorados pelo build do Docker
├── .env.example           # Modelo das variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo Git (.env, venv, etc.)
├── docker-compose.yml     # Orquestração dos containers (App + PostgreSQL)
├── Dockerfile             # Definição do container da aplicação Python
├── main.py                # Script principal do pipeline
└── requirements.txt       # Dependências do projeto
```
