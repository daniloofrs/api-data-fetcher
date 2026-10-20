# API Data Fetcher

Pipeline automatizado para extração, processamento e armazenamento de dados de câmbio de moedas (USD, EUR e BTC para BRL) em tempo real, utilizando Python, PostgreSQL e Docker.

### 📸 Demonstração e Evidências

<p align="center">
  <img width="700" alt="Demonstração do pipeline em execução" src="https://github.com/user-attachments/assets/206d890e-96f5-4c5d-bf01-7d061d25d395" />
</p>

<p align="center">
  <sub>Pipeline em tempo real: extração de dados via API REST, persistência em PostgreSQL e append incremental no arquivo CSV.</sub>
</p>


### Execução e Logs
Registro da extração (USD/EUR/BTC), persistência no banco, gravação em disco e agendamento:

<img width="400" alt="Logs de Execução e Agendamento do Pipeline" src="https://github.com/user-attachments/assets/43383327-af0a-4f75-a75d-75b3c96ed44a" />

---

### Histórico Acumulado no CSV
Visualização do acúmulo de dados históricos no arquivo `data/requisicoes.csv`:

<img width="400" alt="Histórico Acumulado no Arquivo CSV" src="https://github.com/user-attachments/assets/b6635d55-7eae-470f-b881-4a80f350696a" />

---

### Infraestrutura com Docker
Containers da aplicação e PostgreSQL operando em segundo plano via Docker Compose:

<img width="400" alt="Containers Docker e Docker Compose UP" src="https://github.com/user-attachments/assets/5b478079-b9a2-4561-a360-34025a15f744" />

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.12 (compatível com 3.11+)
- **Bibliotecas:** requests, psycopg (v3), python-dotenv
- **Banco de Dados:** PostgreSQL
- **Containerização:** Docker e Docker Compose
- **API Externa:** AwesomeAPI (Cotações de Moedas: USD, EUR e BTC)

---

## 📋 Arquitetura e Funcionamento

1. **Extração de Dados:** O coletor consome a API REST da AwesomeAPI obtendo as cotações mais recentes de **USD-BRL**, **EUR-BRL** e **BTC-BRL**.
2. **Parsing e Estruturação:** Trata os dados capturando a moeda (`moeda`), taxa de compra (`valor`), horário original da cotação (`data_hora`) e o timestamp da extração (`data_extracao`).
3. **Persistência Relacional:** Insere os registros na tabela `cotacoes` dentro do banco PostgreSQL (com persistência via volumes Docker).
4. **Armazenamento em CSV:** Salva os registros em modo incremental (*append*) no arquivo estruturado `/data/requisicoes.csv`.
5. **Automação Contínua:** O pipeline opera em loop automático, executando novos ciclos de extração a cada **15 minutos**.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Docker e Docker Compose instalados.
- Git instalado.

### 1. Clonar o repositório
```bash
git clone https://github.com/daniloofrs/api-data-fetcher.git
cd api-data-fetcher
```

### 2. Configurar as variáveis de ambiente
Crie seu arquivo `.env` com base no `.env.example`:
```bash
cp .env.example .env
```

*(Ajuste os valores no `.env` caso queira alterar a senha ou porta do banco)*

### 3. Subir os containers com Docker Compose
```bash
docker compose up -d --build
```

### 4. Acompanhar os logs da aplicação
Para verificar os ciclos e requisições agendadas em tempo real:
```bash
docker logs -f api-fetcher-app
```

### 5. Consultar os dados gravados no PostgreSQL
Acesse o container do banco para consultar a tabela de cotações:
```bash
docker exec -it postgres-db psql -U postgres -d postgres -c "SELECT * FROM cotacoes ORDER BY id DESC LIMIT 10;"
```
*(Nota: caso tenha modificado o `DB_USER` ou `DB_NAME` no `.env`, ajuste os parâmetros `-U` e `-d` de acordo)*

### 6. Executar análise estatística dos dados
Para visualizar um resumo estatístico das cotações acumuladas (total de registros, mínima, máxima, média e volatilidade):

```bash
# Executando dentro do container da aplicação:
docker exec -it api-fetcher-app python analytics.py
```
*(Ou localmente com Python instalado: `python analytics.py`)*

---

## 📁 Estrutura de Arquivos

```text
api-data-fetcher/
├── data/                  # Diretório montado via volume com o CSV gerado
├── .dockerignore          # Arquivos ignorados pelo build do Docker
├── .env.example           # Modelo das variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo Git (.env, venv, etc.)
├── analytics.py           # Análise e estatísticas dos dados persistidos
├── docker-compose.yml     # Orquestração dos containers (App + PostgreSQL)
├── Dockerfile             # Definição do container da aplicação Python
├── main.py                # Script principal do pipeline
└── requirements.txt       # Dependências do projeto
```
