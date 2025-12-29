from BAL.OracleExec import OracleExec
from models.OrderModel import OrderModel
from models.OrderDetailModel import OrderDetailModel
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
        
    def create_order(self, order: OrderModel):
        query="""INSERT INTO APP_SERVICE.ORDERS (id, cusid, empid, orderdatetime)
                 VALUES (APP_SERVICE.seq_orders.NEXTVAL, :cusid, :empid, :orderdatetime)"""
        try:
            self.oracleExec.execute(query,{
                "cusid": order.cus_id,
                "empid": order.emp_id,
                "orderdatetime": order.order_date_time
            })
        except DatabaseError as e:
            raise DatabaseError(f"Error creating order {order.id}: {e}")
        
    def create_order_detail(self, order_detail: OrderDetailModel):
        query="""INSERT INTO APP_SERVICE.ORDERDETAILS (id, orderid, productid, unitprice, quantity)
                 VALUES (APP_SERVICE.seq_orderdetails.NEXTVAL, :orderid, :productid, :unitprice, :quantity)"""
        try:
            self.oracleExec.execute(query,{
                "orderid": order_detail.order_id,
                "productid": order_detail.product_id,
                "unitprice": order_detail.unit_price,
                "quantity": order_detail.quantity
            })
        except DatabaseError as e:
            raise DatabaseError(f"Error creating order detail {order_detail.id}: {e}")