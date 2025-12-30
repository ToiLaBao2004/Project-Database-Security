from oracledb import DatabaseError
from BAL.OracleExec import OracleExec
from models.CustomerModel import CustomerModel
class CustomerService:
    def __init__(self, oracleExec: OracleExec):
        self.oracleExec=oracleExec
        
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
