from flask import Flask, request
from flask_pymongo import PyMongo, ObjectId
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv('.cred')
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'localhost')
mongo = PyMongo(app) 


@app.route('/usuarios', methods=['GET'])
def get_all_users():
    usuarios = mongo.db.usuarios.find()
    lista_usuarios = []
    for usuario in usuarios:
        lista_usuarios.append({
            '_id': str(usuario['_id']),
            'nome': usuario['nome'],
            'cpf': usuario['cpf'],
            'data_nascimento': usuario['data_nascimento']
        })
    return {'lista': lista_usuarios}, 200



@app.route('/usuarios', methods=['POST'])
def post_user():
    
    data = request.json
    nome = data.get('nome')
    cpf = data.get('cpf')
    data_nascimento = data.get('data_nascimento')


    if not nome or not cpf or not data_nascimento:
        return {'Erro': 'Todos os campos são obrigatórios'}, 400
    if mongo.db.usuarios.find_one({'cpf': cpf}):
        return {'Erro': 'Esse cpf já está cadastrado'}, 400
    
    usuario_id = mongo.db.usuarios.insert_one({
        'nome': nome,
        'cpf': cpf,
        'data_nascimento': data_nascimento
        })

    return {'msg': 'Usuário criado com sucesso!', "id": str(usuario_id.inserted_id)}, 201



@app.route('/usuarios/<id_usuario>', methods=['GET'])
def busca_usuario_por_id(id_usuario):
    usuario = mongo.db.usuarios.find_one({'_id': ObjectId(id_usuario)})
    
    if not usuario:
        return {'Erro': 'Usuário não encontrado!'}, 404
    
    return {
        '_id': str(usuario['_id']),
        'nome':usuario['nome'],
        'cpf': usuario['cpf'],
        'data_nascimento': usuario['data_nascimento']
    }, 200

@app.route('/usuarios/<id_usuario>', methods=['PUT'])
def update_user(id_usuario):
    data = request.json
    nome = data.get('nome')
    cpf = data.get('cpf')
    data_nascimento = data.get('data_nascimento')

    if not nome or not cpf or not data_nascimento :
        return {'Erro': 'Todos os campos são obrigatórios'}, 400
    usuario = mongo.db.usuarios.find_one({'_id': ObjectId(id_usuario)})
    if not usuario:
        return{'Erro': 'Usuário não encontrado!'}, 404
    
    mongo.db.usuarios.update_one(
        {'_id': ObjectId(id_usuario)},
        {'$set': {
            'nome': nome,
            'cpf': cpf,
            'data_nascimento': data_nascimento
        }}
    )

    return {'msg': 'Usuário cadastrado com sucesso!'}, 200



@app.route('/usuarios/<id_usuario>', methods=['DELETE'])
def delete_user(id_usuario):
    usuario = mongo.db.usuarios.find_one({'_id': ObjectId(id_usuario)})

    if not usuario:
        return {'Erro': 'Usuário não encontrado!'}, 404
    
    mongo.db.usuarios.delete_one({'_id': ObjectId(id_usuario)})
    return {'msg': 'Usuário deletado com sucesso!'}, 200


#########################################################################################################################################


@app.route('/bikes', methods=['GET'])
def get_all_bikes():
    marca = request.args.get('marca')
    modelo = request.args.get('modelo')
    cidade = request.args.get('cidade')
    status = request.args.get('status')

    filter = {}
    if marca:
        filter['marca'] = marca
    if modelo:
        filter['modelo'] = modelo
    if cidade:
        filter['cidade'] = cidade
    if status:
        filter['status'] = status

    bikes = mongo.db.bikes.find(filter) 
    lista_bikes = []
    for bike in bikes:
        lista_bikes.append({
            '_id': str(bike['_id']),
            'marca': bike['marca'],
            'modelo': bike['modelo'],
            'cidade': bike['cidade'],
            'status': bike['status']
        })

    return {'lista': lista_bikes}, 200



@app.route('/bikes', methods=['POST'])
def post_bike():
    
    data = request.json
    marca = data.get('marca')
    modelo = data.get('modelo')
    cidade = data.get('cidade')
    status = data.get('status')


    if not marca or not modelo or not cidade or not status:
        return {'Erro': 'Todos os campos são obrigatórios'}, 400
    
    
    bike_id = mongo.db.bikes.insert_one({
        'marca': marca,
        'modelo': modelo,
        'cidade': cidade,
        'status': status
        })

    return {'msg': 'Bike criada com sucesso!', "id": str(bike_id.inserted_id)}, 201


@app.route('/bikes/<id_bike>', methods=['GET'])
def busca_bike_por_id(id_bike):
    bike = mongo.db.bikes.find_one({'_id': ObjectId(id_bike)})
    
    if not bike:
        return {'Erro': 'Bike não encontrada!'}, 404
    
    return {
        '_id': str(bike['_id']),
        'marca':bike['marca'],
        'modelo': bike['modelo'],
        'cidade': bike['cidade'],
        'status': bike['status']
    }, 200


@app.route('/bikes/<id_bike>', methods=['PUT'])
def update_bike(id_bike):
    data = request.json
    marca = data.get('marca')
    modelo = data.get('modelo')
    cidade = data.get('cidade')
    status = data.get('status')

    if not marca or not modelo or not cidade or not status :
        return {'Erro': 'Todos os campos são obrigatórios'}, 400
    bike = mongo.db.bikes.find_one({'_id': ObjectId(id_bike)})
    if not bike:
        return{'Erro': 'Bike não encontrada!'}, 404
    
    mongo.db.bikes.update_one(
        {'_id': ObjectId(id_bike)},
        {'$set': {
            'marca': marca,
            'modelo': modelo,
            'cidade': cidade,
            'status': status
        }}
    )

    return {'msg': 'Bike atualizada com sucesso!'}, 200 
    

@app.route('/bikes/<id_bike>', methods=['DELETE'])
def delete_bike(id_bike):
    bike = mongo.db.bikes.find_one({'_id': ObjectId(id_bike)})

    if not bike:
        return {'Erro': 'Bike não encontrada!'}, 404
    
    mongo.db.bikes.delete_one({'_id': ObjectId(id_bike)})
    return {'msg': 'Bike deletada com sucesso!'}, 200


#######################################################################################################################################


@app.route('/emprestimos', methods=['GET'])
def get_all_emprestimos():
    emprestimos = mongo.db.emprestimos.find()

    lista_emprestimos = []
    for emprestimo in emprestimos:
        emprestimo['_id'] = str(emprestimo['_id'])
        emprestimo['id_usuario'] = str(emprestimo['id_usuario'])
        emprestimo['id_bike'] = str(emprestimo['id_bike'])
        lista_emprestimos.append(emprestimo)

    return {'lista': lista_emprestimos}



@app.route('/emprestimos/usuarios/<id_usuario>/bikes/<id_bike>', methods=['POST'])
def post_emprestimo(id_usuario, id_bike):
    
   
    usuario = mongo.db.usuarios.find_one({'_id': ObjectId(id_usuario)})
    bike = mongo.db.bikes.find_one({'_id': ObjectId(id_bike)})

    if not usuario:
        return {'Erro': 'Usuário não encontrado!'}, 404

    if not bike:
        return {'Erro': 'Bicicleta não encontrada!'}, 404


    if bike.get('status') == 'em uso':
        return {'Erro': 'A bicicleta já está alugada!'}, 400

    mongo.db.bikes.update_one(
        {'_id': ObjectId(id_bike)}, 
        {'$set': {'status': 'em uso'}}
    )

    emprestimo_id = mongo.db.emprestimos.insert_one({
        'id_usuario': id_usuario,
        'id_bike': id_bike,
        'data': request.json.get('data', '')
    }).inserted_id

    return {'msg': 'Empréstimo registrado com sucesso!', 'id_emprestimo': str(emprestimo_id)}, 201 

    



@app.route('/emprestimos/<id_emprestimo>', methods=['DELETE'])
def delete_emprestimo (id_emprestimo) :
    emprestimo = mongo.db.emprestimos.find_one({'_id': ObjectId(id_emprestimo)})

    if not emprestimo:
        return {'Erro': 'Empréstimo não encontrado'}, 404
    
    mongo.db.bikes.update_one(
        {'_id': ObjectId(emprestimo['id_bike'])},
        {'$set': {'status': 'disponivel'}}
    )

    mongo.db.emprestimos.delete_one({'_id': ObjectId(id_emprestimo)})

    return {'msg': 'Empréstimo deletado com sucesso!'}, 200




if __name__ == '__main__':
    app.run(debug=True)