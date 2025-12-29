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
        
        try:
            self.oracleExec.execute(create_user_query, {
                "username": employee.username,
                "password": employee.password
            })

            self.oracleExec.execute(grant_session_query, {"username": employee.username})
            
            self.oracleExec.execute(apply_role_query, {"username": employee.username})
            
            # Insert vào bảng EMPLOYEES
            insert_query = """INSERT INTO APP_SERVICE.EMPLOYEES 
                              (name, dateOfBirth, gender, address, phoneNumber, email, username, emp_role) 
                              VALUES (:name, :dateOfBirth, :gender, :address, :phoneNumber, :email, :username, :emp_role);"""
            
            # Thực thi insert và lấy ID mới
            self.oracleExec.execute(insert_query, {
                "name": employee.name,
                "dateOfBirth": employee.dateOfBirth,
                "gender": employee.gender,
                "address": employee.address,
                "phoneNumber": employee.phoneNumber,
                "email": employee.email,
                "username": employee.username,
                "emp_role": employee.emp_role
            })
            
            self.oracleExec.commit() 
            
        except DatabaseError as e:
            self.oracleExec.rollback()
            raise DatabaseError(f"Error creating employee {employee.username}: {e}")
        
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
        