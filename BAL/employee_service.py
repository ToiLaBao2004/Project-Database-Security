from DAL.db_repository import OracleExec
from DAL.db_connect import get_connection
from models.employee_model import EmployeeModel
from oracledb import DatabaseError,Connection
from configs.settings import settings
import oracledb

class EmployeeService:
    def __init__(self, conn: Connection):
        self.orcl_exec= OracleExec(conn)
        
    def create_employee(self, employee: EmployeeModel):
        
        create_user_query = """CREATE USER :username IDENTIFIED BY :password 
                    DEFAULT TABLESPACE users QUOTA 50M ON users"""
                    
        grant_session_query= """GRANT CREATE SESSION TO :username"""
        
        apply_role_query= """ALTER USER :username DEFAULT ROLE app_user_role;"""
        
        emp_username= "EMP_"+employee.username         
            
        try:
                admin_conn=get_connection(settings.SYS_USER,
                                               settings.SYS_PASSWORD,
                                               mode=oracledb.AUTH_MODE_SYSDBA)
                
                orcl_admin_exec=OracleExec(admin_conn)
                
                orcl_admin_exec.execute(create_user_query, {"username": emp_username,
                                                        "password": employee.password})
                
                orcl_admin_exec.execute(grant_session_query, {"username": emp_username})
                
                orcl_admin_exec.execute(apply_role_query,{"username": emp_username})
        
        except DatabaseError as e:
            raise DatabaseError(f"Error creating employee {employee.username} ",e)
        
        finally:
            admin_conn.close()
        
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
            self.orcl_exec.execute(query,{"name":employee.name,
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
                return self.orcl_exec.fetch_all(query)
            else:
                query=f"""SELECT * FROM APP_SERVICE.EMPLOYEES WHERE :keyword= {type_search}"""
                return self.orcl_exec.fetch_all(query,{"keyword":keyword})
        except DatabaseError as e:
            raise ValueError("Cannot get employee info" ,e)
        
    
        
        
        