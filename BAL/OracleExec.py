from oracledb import Connection
class OracleExec:
    def __init__(self, conn: Connection):
        self.conn = conn
    
    # hỗ trợ chuyển đổi kết quả truy vấn thành dict
    def _dict_factory(self,cursor):
        if cursor.description:
            columns = [col[0].lower() for col in cursor.description]
            cursor.rowfactory = lambda *args: dict(zip(columns, args))
    
    # thường dùng cho truy vấn loại: SELECT MANY
    def fetch_all(self, query: str, params=None) -> list:
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params or {})
            self._dict_factory(cursor)
            return cursor.fetchall()
        finally:
            cursor.close()
    
    # thường dùng cho truy vấn loại: SELECT ONE
    def fetch_one(self, query: str, params=None) -> dict:
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params or {})
            self._dict_factory(cursor)
            return cursor.fetchone()
        finally:
            cursor.close()
    
    # thường dùng cho truy vấn loại: INSERT, UPDATE, DELETE
    def execute(self, query: str, params=None) -> int:
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params or {})
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def execute_many(self, query: str, param_list: list) -> int:
        cursor = self.conn.cursor()
        try:
            cursor.executemany(query, param_list)
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()