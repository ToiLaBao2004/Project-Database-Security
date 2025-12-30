from BAL.OracleExec import OracleExec
from models.CustomerModel import CustomerModel
from oracledb import DatabaseError

class CustomerService:
    def __init__(self, oracleExec: OracleExec):
        self.oracleExec = oracleExec

    def get_all_customers(self):
        """Lấy danh sách tất cả khách hàng"""
        query = """SELECT id, name, phoneNumber, email, dateOfBirth, gender 
                   FROM APP_SERVICE.CUSTOMERS 
                   ORDER BY id DESC"""
        try:
            result = self.oracleExec.execute(query, {})
            customers = []
            if result:
                for row in result:
                    customer = {
                        'id': row[0],
                        'name': row[1],
                        'phone_number': row[2],
                        'email': row[3],
                        'date_of_birth': row[4],
                        'gender': row[5]
                    }
                    customers.append(customer)
            return customers
        except DatabaseError as e:
            raise DatabaseError(f"Error getting customers: {e}")

    def search_customers(self, search_term):
        """Tìm kiếm khách hàng theo tên, số điện thoại hoặc email"""
        query = """SELECT id, name, phoneNumber, email, dateOfBirth, gender 
                   FROM APP_SERVICE.CUSTOMERS 
                   WHERE LOWER(name) LIKE LOWER(:search_term) 
                   OR phoneNumber LIKE :search_term 
                   OR LOWER(email) LIKE LOWER(:search_term)
                   ORDER BY id DESC"""
        try:
            search_pattern = f"%{search_term}%"
            result = self.oracleExec.execute(query, {"search_term": search_pattern})
            customers = []
            if result:
                for row in result:
                    customer = {
                        'id': row[0],
                        'name': row[1],
                        'phone_number': row[2],
                        'email': row[3],
                        'date_of_birth': row[4],
                        'gender': row[5]
                    }
                    customers.append(customer)
            return customers
        except DatabaseError as e:
            raise DatabaseError(f"Error searching customers: {e}")

    def get_customer_by_id(self, customer_id):
        """Lấy thông tin chi tiết một khách hàng"""
        query = """SELECT id, name, phoneNumber, email, dateOfBirth, gender 
                   FROM APP_SERVICE.CUSTOMERS 
                   WHERE id = :customer_id"""
        try:
            result = self.oracleExec.execute(query, {"customer_id": customer_id})
            if result and len(result) > 0:
                row = result[0]
                return {
                    'id': row[0],
                    'name': row[1],
                    'phone_number': row[2],
                    'email': row[3],
                    'date_of_birth': row[4],
                    'gender': row[5]
                }
            return None
        except DatabaseError as e:
            raise DatabaseError(f"Error getting customer: {e}")
