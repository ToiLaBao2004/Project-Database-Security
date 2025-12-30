from BAL.OracleExec import OracleExec
from models.EmployeeModel import EmployeeModel
from oracledb import DatabaseError

class ProductService:
    def __init__(self, oracleExec: OracleExec):
        self.oracleExec = oracleExec

    def get_all_products(self, keyword="", type_search=None):
        
        try:
            if type_search is None:
                query="""SELECT * FROM APP_SERVICE.PRODUCTS WHERE ACTIVE=true order BY id"""
                return self.oracleExec.fetch_all(query)
            else:
                query=f"""SELECT * FROM APP_SERVICE.PRODUCTS WHERE LOWER({type_search}) LIKE :keyword"""
                return self.oracleExec.fetch_all(query,{"keyword":f"%{keyword.lower()}%"})
        except DatabaseError as e:
            raise ValueError("Cannot get product info" ,e)
        
    def create_product(self, product):
        query = """INSERT INTO APP_SERVICE.PRODUCTS 
                   (id, name, image, unitprice, stockquantity, categoryid, brandid, active) 
                   VALUES (APP_SERVICE.seq_products.NEXTVAL, :name, :image, :unitprice, :stockquantity, :categoryid, :brandid, :active)"""
        try:
            self.oracleExec.execute(query, {
                "name": product.name,
                "image": product.image,
                "unitprice": product.unit_price,
                "stockquantity": product.stock_quantity,
                "categoryid": product.category_id,
                "brandid": product.brand_id,
                "active": product.active
            })
        except DatabaseError as e:
            raise DatabaseError(f"Error creating product {product.name}: {e}")
        
    def create_product(self, product):
        query = """INSERT INTO APP_SERVICE.PRODUCTS 
                   (id, name, image, unitprice, stockquantity, categoryid, brandid, active) 
                   VALUES (APP_SERVICE.seq_products.NEXTVAL, :name, :image, :unitprice, :stockquantity, :categoryid, :brandid, :active)"""
        try:
            self.oracleExec.execute(query, {
                "name": product.name,
                "image": product.image,
                "unitprice": product.unit_price,
                "stockquantity": product.stock_quantity,
                "categoryid": product.category_id,
                "brandid": product.brand_id,
                "active": product.active
            })
        except DatabaseError as e:
            raise DatabaseError(f"Error creating product {product.name}: {e}")
        
        
        
    def update_product(self, product):
        query="""UPDATE APP_SERVICE.PRODUCTS SET 
                                                name=:name,
                                                image=:image,
                                                unitprice=:unitprice,
                                                stockquantity=:stockquantity,
                                                categoryid=:categoryid,
                                                brandid=:brandid,
                                                active=:active
                                                WHERE id=:product_id"""
        try:
            self.oracleExec.execute(query,{
                                           "name":product.name,
                                           "image":product.image,
                                           "unitprice":product.unit_price,
                                           "stockquantity":product.stock_quantity,
                                           "categoryid":product.category_id,
                                           "brandid":product.brand_id,
                                           "active":product.active,
                                           "product_id":product.id})
        except DatabaseError as e:
            raise DatabaseError (f"Error updating product ID {product.id} ",e)
        
    def deactivate_product(self, product_id: int):
        query="""UPDATE APP_SERVICE.PRODUCTS SET 
                                                ACTIVE=false
                                                WHERE id=:product_id"""
        try:
            self.oracleExec.execute(query,{"product_id":product_id})
        except DatabaseError as e:
            raise DatabaseError (f"Error deactivating product ID {product_id} ",e)
        
    def get_product_for_order(self, keyword : str=""):
        try:
            if keyword:
                
                query=f"""SELECT id,
                                name,
                                unitPrice,
                                stockQuantity
                                FROM APP_SERVICE.PRODUCTS WHERE LOWER(name) LIKE :keyword order BY id"""
                return self.oracleExec.fetch_all(query,{"keyword":f"%{keyword.lower()}%"})
            
            else:
                query=f"""SELECT id,
                                name,
                                unitPrice,
                                stockQuantity
                                FROM APP_SERVICE.PRODUCTS order BY id"""
                
                return self.oracleExec.fetch_all(query,{})
        except DatabaseError as e:
            raise ValueError("Cannot get product info" ,e)