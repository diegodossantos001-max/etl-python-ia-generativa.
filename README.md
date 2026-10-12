# Explorando IA Generativa em um Pipeline de ETL com Python

Projeto desenvolvido para o desafio do Bootcamp TOTVS de Engenharia de Dados e Machine Learning, com foco nos fundamentos de ETL: Extração, Transformação e Carregamento.

O pipeline extrai dados de clientes fictícios de um arquivo CSV, valida e trata esses dados, gera mensagens personalizadas com a API da OpenAI e salva os resultados em um banco SQLite.

## Adaptação do desafio

O desafio original utilizava a API da Santander Dev Week 2023 para consultar usuários e atualizar suas informações. Como essa API foi descontinuada, o projeto foi adaptado para utilizar:

- **CSV** como fonte dos dados.
- **API da OpenAI** para gerar mensagens.
- **SQLite** para armazenar os dados tratados e as mensagens.

Essa adaptação preserva o objetivo de aplicar as três etapas de um pipeline ETL.

## Etapas do pipeline

### Extração

Leitura do arquivo `data/usuarios.csv` com pandas e conversão dos registros em uma lista de dicionários.

Os números de conta, agência e cartão são lidos como texto para preservar zeros iniciais e máscaras.

### Transformação

Validação e tratamento dos dados:

- Verificação de campos obrigatórios.
- Validação de IDs inteiros positivos e identificação de IDs de usuário duplicados.
- Remoção de espaços nas extremidades dos campos textuais.
- Conversão de saldos e limites para valores numéricos finitos.
- Rejeição de limites negativos, permitindo saldos negativos.

Após a validação, o modelo `gpt-4o-mini` gera uma mensagem para cada usuário válido. As instruções solicitam mensagens em português, com o nome do cliente, incentivando planejamento financeiro e o hábito de poupar, sem inventar produtos, taxas ou prometer rendimentos.

O código rejeita respostas vazias ou com mais de **150 caracteres**, contando espaços. A personalização utiliza o nome do cliente; os dados de conta e cartão não são enviados ao modelo.

### Carregamento

Gravação dos usuários com mensagens válidas na tabela `usuarios`, no banco `data/marketing.db`.

O ID do usuário é a chave primária. Ao carregar novamente um ID existente, o registro é substituído, evitando duplicação desse ID. Usuários sem mensagem válida são ignorados nessa etapa.

## Tecnologias utilizadas

- Python
- pandas
- OpenAI Python SDK
- python-dotenv
- SQLite, por meio do módulo `sqlite3` do Python

## Estrutura do projeto

```text
├── data/
│   └── usuarios.csv
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

O arquivo `.env` é configurado localmente. O banco `data/marketing.db` é criado automaticamente durante o carregamento. Ambos são excluídos do versionamento pelo `.gitignore`.

## Como executar

É necessário ter Python instalado e uma chave da API da OpenAI com acesso ao modelo e créditos disponíveis.

Na raiz do projeto, instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Copie o arquivo de configuração de exemplo:

```powershell
Copy-Item .env.example .env
```

Edite o `.env` e preencha sua chave:

```dotenv
OPENAI_API_KEY=sua_chave_aqui
```

Execute o pipeline:

```powershell
python main.py
```

A execução mostra os usuários válidos, as mensagens geradas e suas quantidades de caracteres. Os registros com mensagens válidas são salvos no SQLite.

Cada execução gera novas chamadas à API, que podem gerar custos, e as mensagens podem variar entre execuções.

## Como consultar o resultado

Após executar o pipeline, utilize este comando na raiz do projeto:

```powershell
python -c "import sqlite3; c = sqlite3.connect('data/marketing.db'); print(c.execute('SELECT id, name, mensagem FROM usuarios ORDER BY id').fetchall()); c.close()"
```

A consulta mostra os registros armazenados sem realizar novas chamadas à OpenAI.

## Verificações realizadas

Durante o desenvolvimento, foram realizados testes manuais das regras de validação e consultas ao banco para conferir a persistência dos dados.

Na execução verificada, foram armazenados cinco usuários com mensagens de até 150 caracteres. Os números de conta e agência preservaram os zeros iniciais, e os saldos e limites consultados corresponderam ao CSV.

## Limitações

O projeto tem finalidade educacional. A validação dos números de conta, agência e cartão verifica apenas se os valores são textos preenchidos e remove espaços nas extremidades. Os zeros iniciais e a máscara do cartão são preservados.

Não são verificados o tamanho desses campos, a quantidade de dígitos, a posição dos separadores nem o formato da máscara do cartão. Portanto, um texto com máscara incompleta pode ser aceito, desde que não esteja vazio.

Essa simplificação mantém o foco nos fundamentos de ETL. A validação de formatos específicos pode ser implementada como melhoria futura.

As instruções orientam o conteúdo das mensagens; a validação automática da resposta verifica apenas preenchimento e tamanho. Falhas de conexão ou da API ainda podem interromper a execução.

## Dados e credenciais

Todos os clientes e dados financeiros utilizados são fictícios e foram criados para fins educacionais. As mensagens geradas são exemplos de comunicação e não constituem recomendações financeiras individualizadas.

A chave da OpenAI deve permanecer no arquivo `.env` local e nunca deve ser publicada no GitHub. O `.env.example` contém apenas o nome da variável, sem credenciais.