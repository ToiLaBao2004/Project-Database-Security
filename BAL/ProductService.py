from BAL.OracleExec import OracleExec
from models.EmployeeModel import EmployeeModel
from oracledb import DatabaseError

class ProductService:
    def __init__(self, oracleExec: OracleExec):
        self.oracleExec = oracleExec

    def get_all_products(self, keyword="", type_search=None):
        
        try:
            if type_search is None:
                query="""SELECT * FROM APP_SERVICE.PRODUCTS WHERE ACTIVE=true"""
                return self.oracleExec.fetch_all(query)
            else:
                query=f"""SELECT * FROM APP_SERVICE.PRODUCTS WHERE :keyword= {type_search}"""
                return self.oracleExec.fetch_all(query,{"keyword":keyword})
        except DatabaseError as e:
            raise ValueError("Cannot get product info" ,e)
        
    def deactivate_product(self, product_id: int):
        query="""UPDATE APP_SERVICE.PRODUCTS SET 
                                                ACTIVE=false
                                                WHERE id=:product_id"""
        try:
            self.oracleExec.execute(query,{"product_id":product_id})
        except DatabaseError as e:
            raise DatabaseError (f"Error deactivating product ID {product_id} ",e)
        