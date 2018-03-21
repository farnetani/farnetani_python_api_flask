from app import db
from app import manager

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logradouro = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    bairro = db.Column(db.String(50))

db.create_all()
manager.create_api(Endereco, collection_name='endereco', methods=['POST','DELETE','PUT','GET'])
# collection_name = 'nome da tabela no banco de dados'