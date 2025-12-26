from DAL.db_connect import get_connection

def login(username, password):
    return get_connection(username, password)
