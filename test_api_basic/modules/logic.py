import json
import os
from flask import abort

current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_all_users = os.path.abspath(os.path.join(current_dir, '..', 'data', 'users', 'users.json'))
path_to_secrets = os.path.abspath(os.path.join(current_dir, '..', 'data', 'secrets.json'))

def check_if_data_valid(data):
    if('name' in data and 'zip' in data and 'street' in data):
        return True
    return False

def get_all_users_from_json_database():
    try:
        if(not os.path.exists(path_to_all_users)):
            return {}
        with open(path_to_all_users, 'r') as data_file:
            data = json.load(data_file)
            return dict(data)
    except Exception as ex:
        abort(500)

def get_token():
    return __get_from_secrets("token")

def __get_from_secrets(key_name):
    with open(path_to_secrets, 'r') as secrets_file:
        data = json.load(secrets_file)
        return data[key_name]