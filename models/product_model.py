import sqlite3
from config1.config import *

class ProductModel:
    def __init__(self):
        self.id_bar = None
        self.db_name = DATABASE_NAME
        self.connect_db()
    def connect_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {PRODUCT_TABLE_NAME} (
                                            {PRODUCT_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                                            {PRODUCT_CODE} TEXT UNIQUE,
                                            {PRODUCT_ID_BARCODE} INTEGER,
                                            {PRODUCT_NAME} TEXT UNIQUE,
                                            {PRODUCT_PRICE} REAL,
                                            {PRODUCT_STOCK} INTEGER,
                                            {PRODUCT_TYPE} TEXT,
                                            {PRODUCT_POINTS} REAL)''')
        conn.commit()
        conn.close()

    def generate_product_code(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX({PRODUCT_ID}) FROM {PRODUCT_TABLE_NAME}")
        max_id = cursor.fetchone()[0]
        conn.close()
        return f"SP{max_id + 1:04d}" if max_id else "SP0001"

    def add_product(self, name, price, stock=None, product_type=None, points=None, id_barcode=None):
        try:
            if self.get_product_by_barcode(id_barcode):  # Truyền id_barcode vào đây
                return False  # Sản phẩm đã tồn tại, không thêm

            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            code = self.generate_product_code()
            cursor.execute(f"""
                INSERT INTO {PRODUCT_TABLE_NAME} 
                ({PRODUCT_CODE}, {PRODUCT_ID_BARCODE}, {PRODUCT_NAME}, {PRODUCT_PRICE}, {PRODUCT_STOCK}, {PRODUCT_TYPE}, {PRODUCT_POINTS}) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                           (code, id_barcode, name, float(price), int(stock) if stock else None, product_type,
                            float(points) if points else None))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Lỗi khi thêm sản phẩm:", e)

    def get_product_by_barcode(self, id_barcode):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {PRODUCT_TABLE_NAME} WHERE {PRODUCT_ID_BARCODE} = ?", (id_barcode,))
        product = cursor.fetchone()
        conn.close()
        return product

    def update_product(self, product_id, name, price, stock, product_type, points):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE {PRODUCT_TABLE_NAME} SET 
            {PRODUCT_NAME}=?, {PRODUCT_PRICE}=?, {PRODUCT_STOCK}=?, {PRODUCT_TYPE}=?, {PRODUCT_POINTS}=? 
            WHERE {PRODUCT_ID}=?""",
            (name, float(price), int(stock), product_type, float(points), product_id))
        conn.commit()
        conn.close()

    def delete_product(self, product_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {PRODUCT_TABLE_NAME} WHERE {PRODUCT_ID}=?", (product_id,))
        conn.commit()
        conn.close()

    def search_product(self, query):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {PRODUCT_TABLE_NAME} WHERE LOWER({PRODUCT_NAME}) LIKE ?", ('%' + query.lower() + '%',))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_all_products(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {PRODUCT_TABLE_NAME}")
        rows = cursor.fetchall()
        conn.close()
        return rows
