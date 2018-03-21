from app import app

# Importando rotas
from app.routes import *

# Importando models
from app.models import endereco # tem que importar primeiro o endereço
from app.models import usuario

if __name__ == '__main__':
    app.run(port=8080, debug=True)
