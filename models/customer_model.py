import sqlite3
import os
from datetime import datetime

from config1.config import DATABASE_NAME


class CustomerModel:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', DATABASE_NAME)
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS customers (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      phone TEXT,
                      address TEXT,
                      points INTEGER DEFAULT 0,
                      created_at TEXT)'''
        self.conn.execute(query)
        self.conn.commit()

    def add_customer(self, name, phone, address):
        if not name:
            return False, "Customer name cannot be empty!"
        try:
            # Lấy thời gian hiện tại
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Gán 10 điểm mặc định khi thêm khách hàng mới
            points = 10
            query = "INSERT INTO customers (name, phone, address, points, created_at) VALUES (?, ?, ?, ?, ?)"
            cursor = self.conn.execute(query, (name, phone, address, points, current_time))
            self.conn.commit()
            return True, "Customer added successfully!"
        except sqlite3.Error as e:
            return False, f"Error adding customer: {e}"

    def update_customer(self, id_kh, name, phone, address):
        if not name:
            return False, "Customer name cannot be empty!"
        try:
            query = "UPDATE customers SET name=?, phone=?, address=? WHERE id=?"
            self.conn.execute(query, (name, phone, address, id_kh))
            self.conn.commit()
            return True, "Customer updated successfully!"
        except sqlite3.Error as e:
            return False, f"Error updating customer: {e}"

    def delete_customer(self, id_kh):
        try:
            query = "DELETE FROM customers WHERE id=?"
            self.conn.execute(query, (id_kh,))
            self.conn.commit()
            return True, "Customer deleted successfully!"
        except sqlite3.Error as e:
            return False, f"Error deleting customer: {e}"

    def search_customer(self, keyword):
        try:
            query = "SELECT * FROM customers WHERE id LIKE ? OR name LIKE ? OR phone LIKE ?"
            return True, self.conn.execute(query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')).fetchall()
        except sqlite3.Error as e:
            return False, f"Error searching customers: {e}"

    def get_all_customers(self):
        try:
            return True, self.conn.execute("SELECT * FROM customers").fetchall()
        except sqlite3.Error as e:
            return False, f"Error retrieving customer list: {e}"

    def close(self):
        self.conn.close()