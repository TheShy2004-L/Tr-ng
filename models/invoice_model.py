import sqlite3
from Entity.Invoice import Invoice
from config1.config import *

class InvoiceModel:
    def __init__(self):
        try:
            self.conn = sqlite3.connect(DATABASE_NAME)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            self.conn = None
            self.cursor = None

    def generate_code(self):
        try:
            self.cursor.execute(f"""SELECT MAX({INVOICE_ID}) FROM {INVOICE_TABLE_NAME}""")
            result = self.cursor.fetchone()
            max_id = result[0] if result[0] else 0

            new_code = f"IV{max_id + 1:03}"

            return new_code
        except sqlite3.Error as e:
            print(f"Error generating code: {e}")
            return None
    def return_product_code(self):
        try:
            self.cursor.execute(f"""SELECT MAX ({INVOICE_ID}) FROM {INVOICE_TABLE_NAME}""")
            result = self.cursor.fetchone()
            max_id = result[0] if result[0] else 0
            new_code = f"IV{max_id:03}"
            return new_code
        except sqlite3.Error as e:
            print(f"Error generating code: {e}")
            return None

    def create_invoice(self):
        try:
            # Chèn một hóa đơn vào cơ sở dữ liệu
            new_code = self.generate_code()
            if new_code:
                sql = f"""INSERT INTO {INVOICE_TABLE_NAME} ({INVOICE_CODE}) VALUES (?)"""
                self.cursor.execute(sql, (new_code,))
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting invoice: {e}")
            self.conn.rollback()

    def update_invoice(self, invoice):
        try:
            sql = f"""
                   UPDATE {INVOICE_TABLE_NAME} SET
                       {INVOICE_EMPLOYEE_CODE} = ?,
                       {INVOICE_CUSTOMER_NAME} = ?,
                       {INVOICE_DATE_CREATED} = ?,
                       {INVOICE_TOTAL_QUANTITY_DRINK} = ?,
                       {INVOICE_TOTAL_QUANTITY_FOOD} = ?, {INVOICE_TOTAL_PRICE_DRINK} = ?,
                       {INVOICE_TOTAL_PRICE_FOOD} = ?, {INVOICE_TOTAL_PRICE} = ?
                   WHERE {INVOICE_CODE} = ?
               """
            self.cursor.execute(sql, tuple(invoice))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating invoice: {e}")
            self.conn.rollback()

    def delete_invoice(self, invoice_code):
        try:
            # Xóa hóa đơn khỏi cơ sở dữ liệu
            sql = f"DELETE FROM {INVOICE_TABLE_NAME} WHERE {INVOICE_CODE} = ?"
            self.cursor.execute(sql, (invoice_code,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting invoice: {e}")
            self.conn.rollback()

    def fetch_invoice(self, invoice_code):
        try:
            # Lấy thông tin hóa đơn từ cơ sở dữ liệu
            sql = f"SELECT * FROM {INVOICE_TABLE_NAME} WHERE {INVOICE_CODE} = ?"
            self.cursor.execute(sql, (invoice_code,))
            row = self.cursor.fetchone()
            if row:
                return Invoice(*row[1:])  # Trả về một đối tượng Invoice
            return None
        except sqlite3.Error as e:
            print(f"Error fetching invoice: {e}")
            return None

    def fetch_all_invoices(self):
        try:
                # Lấy tất cả hóa đơn từ cơ sở dữ liệu
                sql = f"SELECT * FROM {INVOICE_TABLE_NAME}"
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()
                return rows
        except sqlite3.Error as e:
            print(f"Error fetching all invoices: {e}")
            return []

    def get_invoice_by_month(self, month, year):
        try:
            formatted_month = f"{int(month):02d}"  # Đảm bảo luôn có 2 chữ số
            sql = f"SELECT * FROM {INVOICE_TABLE_NAME} WHERE strftime('%Y-%m', {INVOICE_DATE_CREATED}) = '{year}-{formatted_month}'"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows if rows else []
        except sqlite3.Error as e:
            print(f"Error get_invoice_by_month: {e}")
            return []

    def get_invoice_by_day(self,day, month, year):
        try:
            formatted_month = f"{int(month):02d}"  # Đảm bảo luôn có 2 chữ số
            formatted_day = f"{int(day):02d}"
            sql = f"SELECT * FROM {INVOICE_TABLE_NAME} WHERE strftime('%Y-%m-%d', {INVOICE_DATE_CREATED}) = '{year}-{formatted_month}-{formatted_day}'"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows if rows else []
        except sqlite3.Error as e:
            print(f"Error get_invoice_by_month: {e}")
            return []

