import os
import json

config_file_path = './app/core/config.json'

if not os.path.exists(config_file_path):
    print('The config file config.json is missing.')

def get_config_db(filename = config_file_path):
    config = json.loads(open(filename, 'r').read())
    return config.get('api').get('services_db')

cfg = get_config_db()
db_name = cfg.get('NAME')
user = cfg.get('USER')
password = cfg.get('PASSWORD')
hostname = cfg.get('HOST')
port = cfg.get('PORT')

SQLALCHEMY_DB_URL = f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db_name}'