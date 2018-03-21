# API em Flask

Data: 21/03/2018

!!! info "Tutorial passo a passo"

        Tutorial completo em: https://farnetani.github.io/estudos


## Passo a passo que fiz para montar uma App
cd\
c:\
mkdir web-flask
cd web-flask
mkdir api-flask
cd api-flask

***

## Criando o Virtual Env
python -m venv venv

## Ativando o Virtual Env
venv\scripts\activate

***

## Instalando o gerenciador de pacotes: pipenv (melhor que pip)
pip install pipenv

***

## Instalando as libs que usaremos
pipenv install flask # Dispensa comentários
pipenv install flask-sqlalchemy # Para gerenciar o banco de dados
pipenv install flask-restless # Para gerar o CRUD através de nossos models
pipenv install flask-login # Para gerar a autenticação

***

## Criando os arquivos e a estrutura de diretórios:

1. Criar o arquivo run.py na raiz do projeto.
2. Criar a pasta app.
3. Criar as subpastas: models e routes em app.

```dos
    app\models
    app\routes
```

4. Criar em cada pasta o arquivo: **`__init__.py`** para determinar que cada pasta será um módulo.

```dos
    app\models\__init__.py
    app\routes\__init__.py
    app\__init__.py
    run.py
```

## Conteúdo dos arquivos de cada pasta:

**`app/__init__.py`**

    #!python
    from flask import Flask

    app = Flask(__name__)

**`run.py`**

    #!python
    from app import app

    if __name__ == '__main__':
        app.run(port=8080, debug=True)

**`app/routes/__init__.py`**

    #!python
    from app import app

    @app.route('/')
    def index():
        return "Olá Mundo!"

**`run.py`** (Importar o módulo de rotas)

    #!python hl_lines="4"
    from app import app

    # Importando rotas
    from app.routes import *

    if __name__ == '__main__':
        app.run(port=8080, debug=True)

## Configurando o banco de dados

Criar a pasta: database na raiz do projeto.

No arquivo **`__init__.py`** da pasta **`app`**:

    #!python hl_lines="4 6 7 9 10 11 13"
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/storage.db'
    db = SQLAlchemy(app)

    class Usuario(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        nome = db.Column(db.String(100))

    db.create_all()

## Configurando o Flask-Restless

Importar o APIManager: `from flask_restless import APIManager`
e criar um manager(gerenciador): `manager = APIManager(app, flask_sqlalchemy_db=db)`

Rescrever o arquivo **`__init__.py`**

    #!python hl_lines="3 9"
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_restless import APIManager

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/storage.db'
    db = SQLAlchemy(app)

    manager = APIManager(app, flask_sqlalchemy_db=db)

## Flask-Restless

Cria todos os métodos de CRUD.

***

## Iniciando a aplicação

- Criar o model: **`usuario.py`**:

    #!python hl_lines="12"
    from app import db
    from app import manager

    class Cliente(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        nome = db.Column(db.String(100))
        dt_nascimento = db.Column(db.DateTime)
        cpf = db.Column(db.String(14))
        email = db.Column(db.String(100), unique=True)

    db.create_all()
    manager.create_api(Cliente, methods=['POST', 'GET', 'PUT', 'DELETE'])

***

- Referenciar o model criado em **`__init__.py`**:

    #!python hl_lines="7"
    from app import app

    # Importando rotas
    from app.routes import *

    # Importando models
    from app.models import usuario

    if __name__ == '__main__':
        app.run(port=8080, debug=True)

***

- Se acessarmos agora no navegador:

**`http://localhost:8080/api/cliente`**, veremos que a API está funcionando:

```json
// http://localhost:8080/api/cliente
{
  "num_results": 0,
  "objects": [

  ],
  "page": 1,
  "total_pages": 0
}
```

***

### Observações

Por padrão, o manager do flask-restless irá gerar o nome da rota em minúsculo. O **nome do model** não pode usar **UNDERSCORE**, tem que usar a regra do camelo: `GrupoUsuario` e não `Grupo_Usuario`.

## Testes com Postman


** CREATE: http://localhost:8080/api/cliente**

```python

method: POST
Headers: key = Content-Type | Value = application/json
url: http://localhost:8080/api/cliente
raw
{
	"nome": "Junior",
	"dt_nascimento": "1977-12-31 00:00:00",
	"cpf": "12345678901",
	"email": "farnetani@gmail.com"
}

Result:

{
    "cpf": "12345678901",
    "dt_nascimento": "1977-12-31T00:00:00",
    "email": "farnetani@gmail.com",
    "id": 1,
    "nome": "Junior"
}

```

** GET: http://localhost:8080/api/cliente**

```python

method: GET
Headers: key = Content-Type | Value = application/json
url: http://localhost:8080/api/cliente

Result:

{
    "num_results": 1,
    "objects": [
        {
            "cpf": "12345678901",
            "dt_nascimento": "1977-12-31T00:00:00",
            "email": "farnetani@gmail.com",
            "id": 1,
            "nome": "Junior"
        }
    ],
    "page": 1,
    "total_pages": 1
}

```

## Criando o model **`endereco.py`**

    #python!
    from app import db
    from app import manager

    class Endereco(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        logradouro = db.Column(db.String(100))
        numero = db.Column(db.String(10))
        bairro = db.Column(db.String(50))

    db.create_all()
    manager.create_api(Endereco, methods=['POST','DELETE','PUT','GET'])

## Referenciando a chave no model **`usuario.py`**

    #python!
    endereco_id = db.Column(db.Integer, db.ForeignKey('endereco.id'))
    endereco = db.relationship('Endereco')

***

# Testando com o postman

```python

method: POST
Headers: key = Content-Type | Value = application/json
url: http://localhost:8080/api/endereco
raw
{
	"logradouro": "Rua Jacintho Libanio",
	"numero": "420",
	"bairro": "Sao Carlos"
}

Result:

{
    "bairro": "Sao Carlos",
    "id": 1,
    "logradouro": "Rua Jacintho Libanio",
    "numero": "420"
}
```

# Criando um arquivo em PYTHON de exemplo pra testar as requisições

pipenv install requests

**`exemplo-requisicao.py`**
```
import requests
import json

url = 'http://127.0.0.1:8080/api/cliente'
headers = {'Content-Type': 'application/json'}

filters = [dict(nome='Sauro', op='like', val='%y%')]
params = dict(q=json.dumps(dict(filters=filters)))

response = requests.get(url, params=params, headers=headers)
assert response.status_code == 200
print(response.json())
```

# Links
https://flask-restless.readthedocs.io/en/stable/customizing.html

http://flask-sqlalchemy.pocoo.org/2.3/quickstart/#a-minimal-application