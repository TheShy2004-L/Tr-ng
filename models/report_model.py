import sqlite3
from datetime import datetime
from config1.config import *


def create_report(quantity_drink, total_price_drink, quantity_food, total_price_food, total_product_sold, total_price):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT MAX({REPORT_ID}) FROM {REPORT_TABLE_NAME}")
            last_id = cursor.fetchone()[0]
            new_id = (last_id + 1) if last_id else 1
            report_code = f"RP{new_id:03d}"
            cursor.execute(f'''
                INSERT INTO {REPORT_TABLE_NAME} 
                ({REPORT_CODE}, {REPORT_CREATE_AT}, {REPORT_QUANTITY_DRINK}, {REPORT_TOTAL_PRICE_DRINK}, 
                {REPORT_QUANTITY_FOOD}, {REPORT_TOTAL_PRICE_FOOD}, {REPORT_TOTAL_PRODUCT_SOLD}, {REPORT_TOTAL_PRICE})
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (report_code, datetime.now().strftime(DEFAULT_TIME),
                  quantity_drink, total_price_drink, quantity_food, total_price_food, total_product_sold, total_price))
            conn.commit()
            print("Thêm báo cáo thành công!")
    except sqlite3.Error as e:
        print(f"Lỗi khi thêm báo cáo: {e}")


def update_report(report_id, quantity_drink, total_price_drink, quantity_food, total_price_food, total_product_sold, total_price):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE {REPORT_TABLE_NAME} SET {REPORT_CREATE_AT}=?, {REPORT_QUANTITY_DRINK}=?, {REPORT_TOTAL_PRICE_DRINK}=?, 
                {REPORT_QUANTITY_FOOD}=?, {REPORT_TOTAL_PRICE_FOOD}=?, {REPORT_TOTAL_PRODUCT_SOLD}=?, {REPORT_TOTAL_PRICE}=? 
                WHERE {REPORT_ID}=?
            ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), quantity_drink, total_price_drink, quantity_food, total_price_food, total_product_sold, total_price, report_id))

            conn.commit()
            print(f"Cập nhật báo cáo tháng{datetime.now().month} thành công!")
    except sqlite3.Error as e:
        print(f"Lỗi khi cập nhật báo cáo: {e}")


def remove_report(report_id):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {REPORT_TABLE_NAME} WHERE {REPORT_ID}=?", (report_id,))
            conn.commit()
            print(f"Đã xóa báo cáo có ID: {report_id}")
    except sqlite3.Error as e:
        print(f"Lỗi khi xóa báo cáo: {e}")

def get_list_reports():
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {REPORT_TABLE_NAME}")
            reports = cursor.fetchall()
            return reports if reports else None
    except sqlite3.Error as e:
        print(f"Lỗi khi lấy danh sách báo cáo: {e}")
        return None

def get_list_report_by_month(month, year):
    """Lấy danh sách báo cáo từ database theo tháng và năm"""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM {REPORT_TABLE_NAME}
                WHERE strftime('%Y', {REPORT_CREATE_AT}) = ?
                AND strftime('%m', {REPORT_CREATE_AT}) = ?
            """, (str(year), f"{month:02d}"))
            result = cursor.fetchall()
            return result if result else []
    except sqlite3.Error as e:
        print(f"Lỗi khi lấy report theo tháng trong Model: {e}")
        return []

def search_report_by_code(report_code):
    """Tìm báo cáo theo mã"""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT * FROM {REPORT_TABLE_NAME} WHERE {REPORT_CODE} = ?
            ''', (report_code,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Lỗi khi tìm kiếm báo cáo: {e}")
        return None

def search_report_by_date(day, month, year):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT * FROM {REPORT_TABLE_NAME} 
                WHERE strftime('%d', {REPORT_CREATE_AT}) = ? 
                AND strftime('%m', {REPORT_CREATE_AT}) = ?
                AND strftime('%Y', {REPORT_CREATE_AT}) = ?
            ''', (f"{int(day):02d}", f"{int(month):02d}", str(year)))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Lỗi khi tìm kiếm báo cáo: {e}")
        return None
def get_id_time_now():
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT * FROM {REPORT_TABLE_NAME} 
                WHERE strftime('%m', {REPORT_CREATE_AT}) = ?
                AND strftime('%Y', {REPORT_CREATE_AT}) = ?
            ''',  (f"{datetime.now().month:02d}",str(datetime.now().year)))
            data = cursor.fetchone()
            if data:
                return data[0]
            return None
    except sqlite3.Error as e:
        print(f"Lỗi khi tìm kiếm báo cáo: {e}")
        return None