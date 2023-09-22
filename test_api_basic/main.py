import json
from os import environ
import uuid
from flask import Flask, abort, request, jsonify
from modules.decorator import login_required
from modules.logic import check_if_data_valid, get_all_users_from_json_database, get_token, path_to_all_users

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if('username' in data and
       'password' in data):
            if(data['username']=='admin' and data['password'] == 'masterPass'):
                token = get_token()
                return {'token': token}, 200
            else:
                 return abort(401)

@app.route('/users', methods=['GET'])
@login_required
def get_users():
    if(request.args.get('filter') == 'all'):
        all_comments = get_all_users_from_json_database()
        response = jsonify(all_comments)
    
        return response, 200
    else:
        return {}, 200

@app.route('/users', methods=['POST'])
@login_required
def write_user():
    user_data = request.get_json()
    contracts = user_data['contracts']
    if(len(contracts) < 1 or len(contracts) > 3):
        return {"ERROR":"There are only 1 to 3 contracts allowed."}, 400
    if(not check_if_data_valid(user_data)):
        return {"ERROR": "Data not in the right format"}, 400
    else:
        from random import randint
        id = randint(1000, 9999)
        user_data['id'] = id
        all_users = None
        with open(path_to_all_users, 'r') as data_file:
            all_users = json.load(data_file)
            
            all_users['users'].append(user_data)
        with open(path_to_all_users, 'w') as data_file:
            json.dump(all_users, data_file)

    return {"ID":id}, 201 

@app.route('/users/<id>', methods=['DELETE'])
@login_required
def delete_user(id):
    try:
        id = int(id)
    except:
        return {"ERROR": "ID IS NO INTEGER"}, 400
    all_users = get_all_users_from_json_database()
    for i in range(len(all_users['users'])):
        if 'id' in all_users['users'][i]:
            if(id == all_users['users'][i]['id']):
                del all_users['users'][i]
                with open(path_to_all_users, 'w') as data_file:
                    json.dump(all_users, data_file)
                return {'MESSAGE':'OK'}, 200
        else:
            return abort(500)
    return abort(404)

@app.route('/users/<id>', methods=['GET'])
@login_required
def get_user(id: int):
    try:
        id = int(id)
    except:
        return {"ERROR": "ID IS NO INTEGER"}, 400
    all_users = get_all_users_from_json_database()
    for user in all_users['users']:
        if 'id' in user:
            if(id == user['id']):
                return jsonify(user), 200
        else:
            return abort(500)
    return abort(404)

@app.errorhandler(404)
def not_found_404(exception):
    return {"ERROR": "NOT FOUND"}, 404

@app.errorhandler(401)
def unauth_401(exception):
    return {'ERROR': 'NOT AUTHORIZED'}, 401

if __name__ == '__main__':
    app.config['ENV'] = 'Development'
    app.run(host='127.0.0.1', debug=False)