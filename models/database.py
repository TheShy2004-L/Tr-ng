import sqlite3

from config1.config import *


# ket noi sql
def connect_db():
    return sqlite3.connect(DATABASE_NAME)

#khoi tao database
def initialize_db():
    with connect_db() as conn:
        cursor = conn.cursor()

        # Bảng Khách hàng
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {CUSTOMER_TABLE_NAME} (
                {CUSTOMER_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {CUSTOMER_CODE} TEXT UNIQUE NOT NULL,
                {CUSTOMER_NAME} TEXT NOT NULL,
                {CUSTOMER_PHONE} TEXT NOT NULL,
                {CUSTOMER_POINT} INTEGER DEFAULT 0
            )
        ''')

        # Bảng Sản phẩm
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {PRODUCT_TABLE_NAME} (
                                    {PRODUCT_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                                    {PRODUCT_CODE} TEXT UNIQUE,
                                    {PRODUCT_NAME} TEXT UNIQUE,
                                    {PRODUCT_PRICE} REAL,
                                    {PRODUCT_STOCK} INTEGER,
                                    {PRODUCT_TYPE} TEXT,
                                    {PRODUCT_POINTS} REAL,
                                    {PRODUCT_ID_BARCODE} INTEGER
                                    )''')

        # Tạo bảng Hóa đơn
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {INVOICE_TABLE_NAME} (
                {INVOICE_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {INVOICE_EMPLOYEE_CODE} TEXT ,
                {INVOICE_DATE_CREATED} TEXT ,
                {INVOICE_CUSTOMER_NAME} TEXT ,
                {INVOICE_TOTAL_QUANTITY_DRINK} INTEGER DEFAULT 0,
                {INVOICE_TOTAL_QUANTITY_FOOD} INTEGER DEFAULT 0,
                {INVOICE_TOTAL_PRICE_DRINK} REAL DEFAULT 0,
                {INVOICE_TOTAL_PRICE_FOOD} REAL DEFAULT 0,
                {INVOICE_TOTAL_PRICE} REAL DEFAULT 0,
                {INVOICE_CODE} TEXT UNIQUE NOT NULL)
                
        ''')

        # Tạo bảng Chi Tiết Hóa Đơn
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {INVOICE_DETAIL_TABLE_NAME} (
                {INVOICE_DETAIL_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {INVOICE_DETAIL_INVOICE_CODE} TEXT NOT NULL,
                {INVOICE_DETAIL_PRODUCT_NAME} TEXT NOT NULL,
                {INVOICE_DETAIL_PRODUCT_TYPE} TEXT NOT NULL,
                {INVOICE_DETAIL_QUANTITY} INTEGER NOT NULL,
                {INVOICE_DETAIL_PRICE} REAL NOT NULL,
                {INVOICE_DETAIL_SUBTOTAL} REAL NOT NULL,
                {INVOICE_DETAIL_CUSTOMER_NAME} TEXT NOT NULL,
                {INVOICE_DETAIL_PRODUCT_ID_BARCODE} INTEGER NOT NULL,
                FOREIGN KEY ({INVOICE_DETAIL_INVOICE_CODE}) REFERENCES {INVOICE_TABLE_NAME}({INVOICE_CODE})
                )
        ''')

        # Bảng Báo cáo
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {REPORT_TABLE_NAME} (
                {REPORT_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {REPORT_CODE} TEXT UNIQUE NOT NULL,
                {REPORT_CREATE_AT} TEXT NOT NULL,
                {REPORT_QUANTITY_DRINK} INTEGER DEFAULT 0,
                {REPORT_TOTAL_PRICE_DRINK} REAL DEFAULT 0,
                {REPORT_QUANTITY_FOOD} INTEGER DEFAULT 0,
                {REPORT_TOTAL_PRICE_FOOD} REAL DEFAULT 0,
                {REPORT_TOTAL_PRODUCT_SOLD} INTEGER DEFAULT 0,
                {REPORT_TOTAL_PRICE} REAL DEFAULT 0
            )
        ''')

        # Thêm một tài khoản nhân viên mặc định
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {EMPLOYEE_TABLE_NAME} (
                {EMPLOYEE_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {EMPLOYEE_CODE} TEXT UNIQUE NOT NULL,
                {EMPLOYEE_USERNAME} TEXT UNIQUE NOT NULL,
                {EMPLOYEE_PASSWORD} TEXT NOT NULL,
                {EMPLOYEE_ADDRESS} TEXT,
                {EMPLOYEE_GENDER} TEXT CHECK({EMPLOYEE_GENDER} IN ('Nam', 'Nữ', 'Khác')),
                {EMPLOYEE_BIRTHDATE} TEXT,
                {EMPLOYEE_PHONE} TEXT UNIQUE,
                {EMPLOYEE_ROLE} TEXT CHECK({EMPLOYEE_ROLE} IN ('admin', 'employee')) NOT NULL
            )
        ''')

        # Kiểm tra và tạo tài khoản admin nếu chưa có
        cursor.execute(f"SELECT * FROM {ACCOUNT_EMPLOYEE_TABLE_NAME} WHERE {ACCOUNT_EMPLOYEE_ROLE} = 'admin'")
        admin_exists = cursor.fetchone()

        if not admin_exists:
            cursor.execute(f'''
                INSERT INTO {ACCOUNT_EMPLOYEE_TABLE_NAME} ({ACCOUNT_EMPLOYEE_USERNAME}, {ACCOUNT_EMPLOYEE_PASSWORD}, {ACCOUNT_EMPLOYEE_ROLE}, {EMPLOYEE_ID})
                VALUES ('admin', '16012004', 'admin', NULL)
            ''')
            print("Tài khoản admin mặc định đã được tạo! (Username: admin, Password: admin123)")


        # Lưu thay đổi và đóng kết nối
        conn.commit()


if __name__ == "__main__":
    initialize_db()
    print("Database đã được khởi tạo thành công!")