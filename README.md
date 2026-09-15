# API Data Fetcher 🚀

Pipeline automatizado para extração, processamento e armazenamento de dados de câmbio de moedas (USD-BRL) em tempo real, utilizando Python, PostgreSQL e Docker.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Bibliotecas:** `requests`, `psycopg` (v3), `python-dotenv`
- **Banco de Dados:** PostgreSQL
- **Containerização:** Docker e Docker Compose
- **API Externa:** [AwesomeAPI - Cotações de Moedas](https://docs.awesomeapi.com.br/api-de-moedas)

---

## 📋 Arquitetura e Funcionamento

1. O script consome os dados mais recentes da cotação USD-BRL via API REST.
2. Faz o parsing dos dados (taxa de compra e data/hora).
3. Salva uma cópia local estruturada em arquivo CSV na pasta `/data`.
4. Persiste os registros em uma tabela relacional (`cotacoes`) dentro do container PostgreSQL com persistência via volumes.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/) instalados.
- [Git](https://git-scm.com/) instalado.

### 1. Clonar o repositório
```bash
git clone [https://github.com/daniloofrs/api-data-fetcher.git](https://github.com/daniloofrs/api-data-fetcher.git)
cd api-data-fetcher