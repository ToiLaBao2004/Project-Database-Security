from BAL.OracleExec import OracleExec
from models.EmployeeModel import EmployeeModel
import datetime
from oracledb import DatabaseError
class UserService:
    def __init__(self, oracleExec: OracleExec):
        self.oracleExec = oracleExec

    def create_employee(self, employee: EmployeeModel):        
        create_user_query = f"""CREATE USER {employee.username} IDENTIFIED BY {employee.password} DEFAULT TABLESPACE users QUOTA 50M ON users"""
                    
        grant_session_query= f"""GRANT CREATE SESSION TO {employee.username}"""
        
        apply_role_query= f"""GRANT app_user_role TO {employee.username}"""
        
        try:
            self.oracleExec.execute(create_user_query, {})

            self.oracleExec.execute(grant_session_query, {})
            
            self.oracleExec.execute(apply_role_query, {})
            
            insert_query = """INSERT INTO APP_SERVICE.EMPLOYEES 
                              (id ,name, dateOfBirth, gender, address, phoneNumber, email, username, emp_role) 
                              VALUES (APP_SERVICE.seq_employees.NEXTVAL, :name, :dateOfBirth, :gender, :address, :phoneNumber, :email, :username, :emp_role)"""
            
            self.oracleExec.execute(insert_query, {
                "name": employee.name,
                "dateOfBirth": employee.dateofbirth,
                "gender": employee.gender,
                "address": employee.address,
                "phoneNumber": employee.phonenumber,
                "email": employee.email,
                "username": employee.username,
                "emp_role": employee.emp_role
            })
            
        except DatabaseError as e:
            raise DatabaseError(f"Error creating employee {employee.username}: {e}")
        
    def update_employee(self, employee: EmployeeModel):
        query="""UPDATE APP_SERVICE.EMPLOYEES SET 
                                                address=:address,
                                                phoneNumber=:phone_number,
                                                email=:email
                                                WHERE id=:employee_id"""
        try:
            self.oracleExec.execute(query,{
                                           "address":employee.address,
                                           "phone_number":employee.phonenumber,
                                           "email":employee.email,
                                           "employee_id":employee.id})
        except DatabaseError as e:
            raise DatabaseError (f"Error updating employee {employee.username} ",e)
        
    def deactive_employee(self, username: str):
        query=f"""ALTER USER {username} ACCOUNT LOCK"""
        
        try:
            self.oracleExec.execute(query,{})
        except DatabaseError as e:
            raise DatabaseError(f"Error LOCKED user {username} ",e)
        
    def get_user_session(self):
        sql = """SELECT
            user AS USERNAME
            FROM dual"""
            
        return self.oracleExec.fetch_one(sql,{})
        
    def get_all_employee_info(self, keyword="", type_search=None):
        try:
            
            username=self.get_user_session()["username"]
            print(username)
            if "EMP" in username:
                query="""SELECT * FROM APP_SERVICE.EMPLOYEES"""
                return self.oracleExec.fetch_all(query,{})
            
            if type_search is None:
                query="""SELECT * FROM APP_SERVICE.EMPLOYEES e WHERE EXISTS (SELECT 1 FROM DBA_USERS u 
                                                                    WHERE u.username = upper(e.username) 
                                                                    AND u.account_status = 'OPEN')"""
                return self.oracleExec.fetch_all(query)
            else:
                query=f"""SELECT * FROM APP_SERVICE.EMPLOYEES WHERE :keyword= {type_search} AND EXISTS 
                                                                    (SELECT 1 FROM DBA_USERS u 
                                                                    WHERE u.username = upper(username) 
                                                                    AND u.account_status = 'OPEN')"""
                return self.oracleExec.fetch_all(query, {"keyword": keyword})
                
        except DatabaseError as e:
            raise ValueError("Cannot get employee info", e)
            