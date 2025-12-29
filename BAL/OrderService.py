from BAL.OracleExec import OracleExec
from models.OrderModel import OrderModel
from oracledb import DatabaseError

class OrderService:
    def __init__(self, oracleExec: OracleExec):
        self.oracleExec = oracleExec

    def load_orders(self, keyword="", type_search=None):
        try:
            if type_search is None:
                query="""SELECT * FROM APP_SERVICE.ORDERS"""
                return self.oracleExec.fetch_all(query)
            else:
                query=f"""SELECT * FROM APP_SERVICE.ORDERS WHERE :keyword= {type_search}"""
                return self.oracleExec.fetch_all(query,{"keyword":keyword})
        except DatabaseError as e:
            raise ValueError("Cannot get order info" ,e)