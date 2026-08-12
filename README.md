# API Data Fetcher — Cotação USD-BRL

Script em Python que consulta a cotação atual do dólar (USD-BRL) via API pública e salva o resultado em um arquivo CSV local.

## O que o script faz

1. Faz uma requisição GET para a AwesomeAPI (`economia.awesomeapi.com.br`), buscando a cotação USD-BRL.
2. Trata falhas de conexão (sem internet, API fora do ar, timeout) sem deixar o programa quebrar sem explicação.
3. Trata respostas de erro da API (status code diferente de 200).
4. Se a requisição for bem-sucedida, exibe a data e o valor da cotação no terminal.
5. Salva a cotação (valor + data) em `data/requisicoes.csv`.

## Tecnologias

- Python 3
- [requests](https://pypi.org/project/requests/) — chamadas HTTP
- `csv` (biblioteca padrão do Python) — escrita do arquivo de saída

## API utilizada

[AwesomeAPI — Economia](https://economia.awesomeapi.com.br/last/USD-BRL) — API pública gratuita de cotações, sem necessidade de chave de autenticação.

## Como rodar

1. Clone o repositório e entre na pasta do projeto.
2. Crie e ative um ambiente virtual:
   ```
   python3 -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Execute o script:
   ```
   python main.py
   ```
5. O resultado aparece no terminal e é salvo em `data/requisicoes.csv`.

## Estrutura do projeto

```
api-data-fetcher/
├── data/
│   └── requisicoes.csv
├── main.py
├── requirements.txt
└── README.md
```

## Aprendizado

Primeiro projeto do módulo "Learn the Basics" do roadmap de Engenharia de Dados — validação prática de consumo de API, tratamento de exceções, manipulação de arquivos e versionamento com Git.