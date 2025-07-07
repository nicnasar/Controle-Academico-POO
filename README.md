# Controle-Academico-POO

Repositório contendo arquivos relacionados ao trabalho de POO.

adicionar criar venv
instalar as bibliotecas no venv


## Passos para rodar o projeto após clonar o repositório:

### 0. Habilite a permissão do PowerShell:
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 1. Ative o ambiente virtual (PowerShell):
`.venv\Scripts\Activate`

### 2. Instale as dependências:
`pip install -r requirements.txt`
> **ou**, se o arquivo estiver em src:
`pip install -r src/requirements.txt`

### 3. (Opcional) Se adicionar novas bibliotecas, gere/atualize o requirements.txt:
`pip freeze > requirements.txt`

### 4. Rode o sistema principal:
`python src/main.py`

### 5. (Se for usar a interface):
`streamlit run src/interface/Dashboard.py`

> Repita os passos 1, 2, 4 e 5 toda vez que for rodar o projeto em uma nova sessão.

# Esse código usa DAO:

## DAO (Data Access Object) com Python e SQLite

### 🧠 O que é DAO na prática?

Imagine que você tem um **restaurante**, e os **dados dos clientes** ficam guardados numa **cozinha (o banco de dados SQLite)**.

Você não quer que qualquer pessoa vá lá na cozinha abrir a geladeira e pegar as coisas — seria bagunça.

Então, você cria uma **pessoa responsável só por conversar com a cozinha**: o garçom. Ele sabe como pedir pratos, buscar pedidos e entregar direitinho. Essa pessoa é o **DAO**.

---

### ✅ Por que usar DAO?

- Seu código principal **não precisa saber como o banco funciona**.
- Você pode **trocar o banco depois** (SQLite por PostgreSQL, por exemplo) **sem mexer no restante da aplicação**.
- O código fica mais **limpo, modular, testável e organizado**.

---

### 📁 Estrutura de Diretórios

```plaintext
app/
├── dao/
│   └── cliente_dao.py
├── modelo/
│   └── cliente.py
└── main.py
```




