from oracledb import DatabaseError
from BAL.OracleExec import OracleExec
from models.CustomerModel import CustomerModel
class CustomerService:
    def __init__(self, oracleExec: OracleExec):
        self.oracleExec=oracleExec
        
    def get_all_customers(self, keyword=None, search_type=None) -> list:
        try:
            if search_type is None:
                query="""SELECT id, name, phoneNumber FROM APP_SERVICE.CUSTOMERS ORDER BY id"""
                
                return self.oracleExec.fetch_all(query,{})
            else:
                query=f"""SELECT id, name, phoneNumber FROM APP_SERVICE.CUSTOMERS
                                                WHERE {search_type} LIKE :keyword
                                                ORDER BY id"""
            
                return self.oracleExec.fetch_all(query,{"keyword":f"%{keyword}%"})
        
        except DatabaseError as e:
            raise ValueError("Can not get customers info ",e)
        
    def get_customer_by_phone(self,phonenumber: str) -> dict|None:
        try:
            query="""SELECT * FROM APP_SERVICE.CUSTOMERS WHERE phoneNumber = :phonenumber"""
            
            return self.oracleExec.fetch_one(query,{"phonenumber":phonenumber})
        except DatabaseError as e:
            raise ValueError("Can not get customer info ",e)
        
    def create_customer(self, customer: CustomerModel):
        
        try:
            query = """INSERT INTO APP_SERVICE.CUSTOMERS (id, name, phoneNumber) 
                   VALUES (APP_SERVICE.seq_customers.NEXTVAL, :name, :phonenumber)
                   RETURNING id INTO :id"""
                        
            return self.oracleExec.execute_with_returning(query,{"name":customer.name,
                                           "phonenumber":customer.phonenumber})
        except DatabaseError as e:
            raise ValueError(f"Can't insert customer with phone number: {customer.phonenumber} ", e)
        
    def set_context(self, phone_number: str):
        try:
            query = """EXEC sec_mgr.fgac_ctx_pkg.set_phonenumber(:phone_number)"""
            
            self.oracleExec.execute(query,{"phone_number":phone_number})
            
            query = """SELECT id, name, phoneNumber FROM APP_SERVICE.CUSTOMERS WHERE phonenumber = :phone_number"""
            
            self.oracleExec.fetch_one(query,{"phone_number":phone_number})
        except DatabaseError as e:
            raise ValueError(f"Can't set context for phone number: {phone_number} ", e)
