import oracledb

def get_connection(username, password):
    return oracledb.connect(
        user=username,
        password=password,
        dsn="localhost:1521/FREEPDB1"
    )