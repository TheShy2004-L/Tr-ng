import sqlite3
from config1.config import *


class InvoiceDetailModel:
    def __init__(self):
        """Khởi tạo DAO với đường dẫn database."""
        self.db_path = DATABASE_NAME

    def connect(self):
        """Kết nối đến SQLite database."""
        return sqlite3.connect(self.db_path)

    def create_invoice_detail(self, invoice_detail):
        """Thêm một hóa đơn chi tiết vào database."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(f'''
                INSERT INTO {INVOICE_DETAIL_TABLE_NAME} (
                    {INVOICE_DETAIL_INVOICE_CODE},{INVOICE_DETAIL_PRODUCT_NAME},{INVOICE_DETAIL_PRODUCT_TYPE}, 
                    {INVOICE_DETAIL_QUANTITY}, {INVOICE_DETAIL_PRICE}, 
                    {INVOICE_DETAIL_SUBTOTAL}, {INVOICE_DETAIL_CUSTOMER_NAME},
                    {INVOICE_DETAIL_PRODUCT_ID_BARCODE}
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                invoice_detail.invoice_code,invoice_detail.product_name,
                invoice_detail.product_type,
                invoice_detail.quantity, invoice_detail.price,
                invoice_detail.subtotal, invoice_detail.customer_name,
                invoice_detail.product_id_barcode
            ))
            conn.commit()
            return cursor.lastrowid  # Trả về ID mới thêm
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm invoice_detail: {e}")
        finally:
            conn.close()

    def update_invoice_detail(self, invoice_code, product_id_barcode, new_data):
        """Cập nhật hóa đơn chi tiết dựa trên mã hóa đơn và mã sản phẩm."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE {INVOICE_DETAIL_TABLE_NAME}
                SET {INVOICE_DETAIL_QUANTITY} = ?, {INVOICE_DETAIL_PRICE} = ?, 
                    {INVOICE_DETAIL_SUBTOTAL} = ?
                WHERE {INVOICE_DETAIL_INVOICE_CODE} = ? AND {INVOICE_DETAIL_PRODUCT_ID_BARCODE} = ?
            ''', (
                new_data["quantity"], new_data["price"], new_data["subtotal"],
                invoice_code, product_id_barcode
            ))
            conn.commit()
            return cursor.rowcount  # Trả về số dòng bị ảnh hưởng
        except sqlite3.Error as e:
            print(f"Lỗi khi cập nhật invoice_detail: {e}")
        finally:
            conn.close()

    def delete_invoice_detail(self, invoice_code, product_id_barcode):
        """Xóa một mục trong bảng invoice_detail."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(f'''
                DELETE FROM {INVOICE_DETAIL_TABLE_NAME}
                WHERE {INVOICE_DETAIL_INVOICE_CODE} = ? AND {INVOICE_DETAIL_PRODUCT_ID_BARCODE} = ?
            ''', (invoice_code, product_id_barcode))
            conn.commit()
            return cursor.rowcount  # Trả về số dòng bị xóa
        except sqlite3.Error as e:
            print(f"Lỗi khi xóa invoice_detail: {e}")
        finally:
            conn.close()

    def fetch_all_by_invoice_code(self, invoice_code):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(f'''SELECT * FROM {INVOICE_DETAIL_TABLE_NAME}
             WHERE {INVOICE_DETAIL_INVOICE_CODE} LIKE ? ''', (invoice_code,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Lỗi khi fetch_all_by_invoice_code invoice_detail: {e}")
        finally:
            conn.close()

    def fetch_all(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(f'''SELECT * FROM {INVOICE_DETAIL_TABLE_NAME} ''')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Lỗi khi fetch_all invoice_detail: {e}")
        finally:
            conn.close()
