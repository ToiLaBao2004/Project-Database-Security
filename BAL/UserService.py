from BAL.OracleExec import OracleExec
from models.EmployeeModel import EmployeeModel
from oracledb import DatabaseError

class UserService:
    def __init__(self, oracleExec: OracleExec):
        self.oracleExec = oracleExec

    def create_employee(self, employee: EmployeeModel):
        
        create_user_query = """CREATE USER :username IDENTIFIED BY :password 
                    DEFAULT TABLESPACE users QUOTA 50M ON users"""
                    
        grant_session_query= """GRANT CREATE SESSION TO :username"""
        
        apply_role_query= """ALTER USER :username DEFAULT ROLE app_user_role;"""
        
        emp_username= "EMP_"+employee.username         

        
    def update_employee(self, employee: EmployeeModel):
        query="""UPDATE APP_SERVICE.EMPLOYEES SET 
                                                name=:name,
                                                dateOfBirth=:date_of_birth,
                                                gender=:gender,
                                                address=:address,
                                                phoneNumber=:phone_number,
                                                email=:email
                                                WHERE id=:employee_id"""
        try:
            self.oracleExec.execute(query,{"name":employee.name,
                                           "date_of_birth":employee.date_of_birth,
                                           "gender":employee.gender,
                                           "address":employee.address,
                                           "phone_number":employee.phone_number,
                                           "email":employee.email,
                                           "employee_id":employee.id})
        except DatabaseError as e:
            raise DatabaseError (f"Error updating employee {employee.username} ",e)
        
    def get_all_employee_info(self, keyword="", type_search=None):
        
        try:
            if type_search is None:
                query="""SELECT * FROM APP_SERVICE.EMPLOYEES"""
                return self.oracleExec.fetch_all(query)
            else:
                query=f"""SELECT * FROM APP_SERVICE.EMPLOYEES WHERE :keyword= {type_search}"""
                return self.oracleExec.fetch_all(query,{"keyword":keyword})
        except DatabaseError as e:
            raise ValueError("Cannot get employee info" ,e)
        