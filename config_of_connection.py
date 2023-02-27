import configparser

def get_conn_params_from_config():
    config = configparser.ConfigParser()
    config.read('database.ini')
    host = config['postgresql']['host']
    database = config['postgresql']['database']
    user = config['postgresql']['user']
    password = config['postgresql']['password']
    return host, database, user, password
