import oracledb

def get_connection(username, password, mode=oracledb.AUTH_MODE_DEFAULT):
        return oracledb.connect(
            user=username,
            password=password,
            dsn="localhost:1521/FREEPDB1",
            mode=mode
        )
