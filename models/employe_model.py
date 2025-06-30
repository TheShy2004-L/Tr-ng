import sqlite3
import random

from config1.config import EMPLOYEE_TABLE_NAME, EMPLOYEE_ID, EMPLOYEE_CODE, EMPLOYEE_USERNAME, EMPLOYEE_PASSWORD, \
    EMPLOYEE_ADDRESS, EMPLOYEE_GENDER, EMPLOYEE_BIRTHDATE, EMPLOYEE_PHONE, EMPLOYEE_ROLE, DATABASE_NAME


class EmployeeModel:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.conn.cursor()

    def generate_code(self):
        try:
            self.cursor.execute(f"""SELECT MAX({EMPLOYEE_ID}) FROM {EMPLOYEE_TABLE_NAME}""")
            result = self.cursor.fetchone()
            max_id = result[0] if result[0] else 0

            new_code = f"NV{max_id + 1:03}"

            return new_code
        except sqlite3.Error as e:
            print(f"Error generating code: {e}")

    def add_employee(self, username, password, address, gender, birthdate, phone, role):
        employee_code = self.generate_code()
        try:
            self.cursor.execute(f'''
                INSERT INTO {EMPLOYEE_TABLE_NAME} ({EMPLOYEE_CODE}, {EMPLOYEE_USERNAME}, {EMPLOYEE_PASSWORD}, {EMPLOYEE_ADDRESS}, {EMPLOYEE_GENDER}, {EMPLOYEE_BIRTHDATE}, {EMPLOYEE_PHONE}, {EMPLOYEE_ROLE})
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (employee_code, username, password, address, gender, birthdate, phone, role))
            self.conn.commit()
            return True, "Thêm nhân viên thành công!"
        except sqlite3.IntegrityError:
            return False, "Tên đăng nhập hoặc số điện thoại đã tồn tại!"

    def get_all_employees(self):
        self.cursor.execute(f"SELECT * FROM {EMPLOYEE_TABLE_NAME}")
        return self.cursor.fetchall()

    def update_employee(self, emp_code,username,password, address, gender, birthdate, phone, role):
        self.cursor.execute(f'''
            UPDATE {EMPLOYEE_TABLE_NAME} 
            SET  {EMPLOYEE_USERNAME} = ?, {EMPLOYEE_PASSWORD} = ?,
                {EMPLOYEE_ADDRESS} = ?, {EMPLOYEE_GENDER} = ?, 
                {EMPLOYEE_BIRTHDATE} = ?, {EMPLOYEE_PHONE} = ?, {EMPLOYEE_ROLE} = ?
            WHERE {EMPLOYEE_CODE} = ?
        ''', (username,password,address, gender, birthdate, phone, role, emp_code))
        self.conn.commit()

    def delete_employee(self, emp_id):
        self.cursor.execute(f"DELETE FROM {EMPLOYEE_TABLE_NAME} WHERE {EMPLOYEE_CODE} = ?", (emp_id,))
        self.conn.commit()

    def search_employee(self, keyword):
        self.cursor.execute(f"SELECT * FROM {EMPLOYEE_TABLE_NAME} WHERE {EMPLOYEE_USERNAME} LIKE ? OR {EMPLOYEE_CODE} LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
        return self.cursor.fetchall()
    def login(self,username,password):
        self.cursor.execute(f"SELECT * FROM {EMPLOYEE_TABLE_NAME} WHERE "
                            f"{EMPLOYEE_USERNAME} LIKE ?"
                            f" AND {EMPLOYEE_PASSWORD} LIKE ?",(username,password))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()

# employee_model = EmployeeModel()
#
# # Danh sách mẫu dữ liệu
# sample_data = [
#     ("nguyenanh01", "123456", "Hà Nội", "Nam", "1995-05-12", "0987654321", "employee"),
#     ("tranmai02", "123456", "Hồ Chí Minh", "Nữ", "1992-07-23", "0912345678", "employee"),
#     ("lehoang03", "123456", "Đà Nẵng", "Nam", "1998-09-15", "0933221100", "employee"),
#     ("phamthuy04", "123456", "Hải Phòng", "Nữ", "1990-11-10", "0978899001", "employee"),
#     ("dangphuc05", "123456", "Cần Thơ", "Nam", "1993-03-30", "0967788992", "employee"),
#     ("vuquynh06", "123456", "Huế", "Nữ", "1997-08-20", "0956677883", "employee"),
#     ("domanh07", "123456", "Bình Dương", "Nam", "1994-06-25", "0945566774", "employee"),
#     ("hoanglan08", "123456", "Nha Trang", "Nữ", "1996-12-05", "0934455665", "employee"),
#     ("admin01", "123456", "Hà Nội", "Nam", "1985-02-15", "0922334455", "admin"),
#     ("admin02", "123456", "Hồ Chí Minh", "Nữ", "1988-04-10", "0911223344", "admin")
# ]
#
# # Thêm dữ liệu vào database
# for data in sample_data:
#     success, message = employee_model.add_employee(*data)
#     print(f"{'✅' if success else '❌'} {message}")