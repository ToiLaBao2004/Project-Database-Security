from DAL.db_repository import execute_query
from DAL.db_connect import get_connection

def login(username, password):
    return get_connection(username, password)

def get_current_user_info(conn):
    sql = """
        SELECT
            user AS USERNAME,
            sys_context('USERENV','SESSION_USER') AS SESSION_USER,
            sys_context('USERENV','CURRENT_USER') AS CURRENT_USER,
            sys_context('USERENV','CON_NAME') AS CONTAINER
        FROM dual
    """
    return execute_query(conn, sql)
