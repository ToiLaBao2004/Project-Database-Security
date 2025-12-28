from DAL.db_connect import get_connection
import oracledb

def login(username, password):
    # Nếu user là SYS, tự động dùng SYSDBA mode
    if username.upper() == 'SYS':
        return get_connection(username, password, mode=oracledb.AUTH_MODE_SYSDBA)
    else:
        return get_connection(username, password)
