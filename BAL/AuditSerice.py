from BAL.OracleExec import OracleExec
from oracledb import DatabaseError

class AuditService:
    def __init__(self, oracleExec: OracleExec):
        self.oracleExec=oracleExec
        
    def get_user_audit(self, username: str) -> list:
        try:
            query = f"""SELECT
                        dbusername as username,
                        event_timestamp,
                        action_name,
                        object_name,
                        return_code
                    FROM unified_audit_trail 
                    WHERE object_schema = 'APP_SERVICE'
                    AND object_name IN ('ORDERS', 'ORDERDETAILS') 
                    AND dbusername = '{username.upper()}
                    ORDER BY event_timestamp DESC'"""
            
            return self.oracleExec.fetch_all(query, {})
        except Exception as e:
            raise Exception(f"Lỗi truy vấn Audit: {str(e)}")