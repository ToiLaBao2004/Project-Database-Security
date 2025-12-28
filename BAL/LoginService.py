from DAL.connectDB import get_connection
from BAL.OracleExec import OracleExec

def login(username, password):
    conn = get_connection(username, password)
    oracleExec = OracleExec(conn)
    return oracleExec