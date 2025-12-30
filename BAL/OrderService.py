from BAL.OracleExec import OracleExec
from models.OrderModel import OrderModel
from models.OrderDetailModel import OrderDetailModel
from oracledb import DatabaseError

class OrderService:
    def __init__(self, oracleExec: OracleExec):
        self.oracleExec = oracleExec
        
    def load_orders(self, keyword="", type_search=None):
        try:
            base_query = """SELECT 
                            o.id AS id, 
                            o.orderDateTime AS order_date, 
                            c.name AS customer_name, 
                            c.phoneNumber AS customer_phone, 
                            e.name AS employee_name, 
                            e.username AS employee_username,
                            (SELECT SUM(od.unitPrice * od.quantity) 
                            FROM APP_SERVICE.ORDERDETAILS od 
                            WHERE od.orderId = o.id) AS total
                        FROM APP_SERVICE.ORDERS o
                        JOIN APP_SERVICE.CUSTOMERS c ON o.cusId = c.id
                        JOIN APP_SERVICE.EMPLOYEES e ON o.empId = e.id
                    """

            if type_search is None:
                query = f"{base_query}"
                return self.oracleExec.fetch_all(query)
            else:
                query = f"""
                    {base_query} 
                    WHERE LOWER({type_search}) LIKE :keyword
                """
                return self.oracleExec.fetch_all(query, {"keyword": f"%{keyword.lower()}%"})

        except DatabaseError as e:
            print(f"Database Error: {e}")
            raise ValueError("Cannot get order info", e)
    
    def load_orders_detail(self, order_id):
        try:
            query="""SELECT 
                    od.id AS id, 
                    od.orderId AS order_id, 
                    p.name AS product_name,
                    od.unitPrice AS unit_price, 
                    od.quantity AS quantity,
                    (od.unitPrice * od.quantity) AS subtotal
                FROM APP_SERVICE.ORDERDETAILS od
                JOIN APP_SERVICE.PRODUCTS p ON od.productId = p.id
                WHERE od.orderId = :order_id"""
                
            return self.oracleExec.fetch_all(query,{"order_id":order_id})
        except DatabaseError as e:
            raise ValueError(f"Can't get order detail of {order_id}")
        
    def create_order(self, order: OrderModel):
        query="""INSERT INTO APP_SERVICE.ORDERS (id, cusId, empId, orderDateTime)
                 VALUES (APP_SERVICE.seq_orders.NEXTVAL, :cusid, :empid, :orderdatetime)
                 RETURNING id INTO :id"""
        try:
            return self.oracleExec.execute_with_returning(query, {
                "cusid": order.cus_id,
                "empid": order.emp_id,
                "orderdatetime": order.order_date_time
            })
        except DatabaseError as e:
            raise DatabaseError(f"Error creating order: {e}")
        
    def create_order_detail(self, order_detail: OrderDetailModel):
        query="""INSERT INTO APP_SERVICE.ORDERDETAILS (id, orderId, productId, unitPrice, quantity)
                 VALUES (APP_SERVICE.seq_orderdetails.NEXTVAL, :orderid, :productid, :unitprice, :quantity)"""
        try:
            self.oracleExec.execute(query,{
                "orderid": order_detail.order_id,
                "productid": order_detail.product_id,
                "unitprice": order_detail.unit_price,
                "quantity": order_detail.quantity
            })
            
            self.buy_product(id=order_detail.product_id, quantity=order_detail.quantity)
            
        except DatabaseError as e:
            raise DatabaseError(f"Error creating order detail order_detail: {e}")
        
        
    def buy_product(self, id, quantity):
        try:
            query = """UPDATE APP_SERVICE.PRODUCTS 
                       SET stockQuantity = stockQuantity - :quantity 
                       WHERE id = :id"""
            
            rows_updated = self.oracleExec.execute(query, {"quantity": quantity, "id": id})
            print(rows_updated)
            
        except Exception as e:
            raise ValueError(f"Cannot update stock quantity of product {id}: {e}")