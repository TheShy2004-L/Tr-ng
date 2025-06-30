import sqlite3
import random
from datetime import datetime, timedelta

from config1.config import (
    DATABASE_NAME,
    INVOICE_TABLE_NAME, INVOICE_ID, INVOICE_CODE, INVOICE_EMPLOYEE_CODE, INVOICE_DATE_CREATED, INVOICE_CUSTOMER_NAME,
    INVOICE_TOTAL_QUANTITY_DRINK, INVOICE_TOTAL_QUANTITY_FOOD, INVOICE_TOTAL_PRICE_DRINK, INVOICE_TOTAL_PRICE_FOOD, INVOICE_TOTAL_PRICE,
    INVOICE_DETAIL_TABLE_NAME, INVOICE_DETAIL_ID, INVOICE_DETAIL_INVOICE_CODE, INVOICE_DETAIL_PRODUCT_ID_BARCODE,
    INVOICE_DETAIL_PRODUCT_NAME, INVOICE_DETAIL_PRODUCT_TYPE, INVOICE_DETAIL_QUANTITY, INVOICE_DETAIL_PRICE,
    INVOICE_DETAIL_SUBTOTAL, INVOICE_DETAIL_CUSTOMER_NAME
)

# Kết nối database
conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

# Danh sách sản phẩm mẫu
products = [
    (1, "ice-cream", "food", 25000),
    (2, "snack", "food", 10000),
    (3, "red-bull", "drink", 18000),

]

# Thời gian bắt đầu từ tháng 1 đến hiện tại
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 3, 15)
delta = timedelta(days=1)
invoice_counter = 1  # Biến đếm hóa đơn

while start_date <= end_date:
    for _ in range(4):  # 4 hóa đơn mỗi ngày
        invoice_code = f"IV{invoice_counter:03d}"
        employee_code = "NV001"
        customer_name = "khách lẻ"
        total_quantity_drink = 0
        total_quantity_food = 0
        total_price_drink = 0
        total_price_food = 0
        total_price = 0

        # Thêm hóa đơn vào bảng Invoice
        cursor.execute(
            f"INSERT INTO {INVOICE_TABLE_NAME} ({INVOICE_CODE}, {INVOICE_DATE_CREATED}, {INVOICE_EMPLOYEE_CODE}, {INVOICE_CUSTOMER_NAME}, "
            f"{INVOICE_TOTAL_QUANTITY_DRINK}, {INVOICE_TOTAL_QUANTITY_FOOD}, {INVOICE_TOTAL_PRICE_DRINK}, {INVOICE_TOTAL_PRICE_FOOD}, {INVOICE_TOTAL_PRICE}) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (invoice_code, start_date.strftime('%Y-%m-%d %H:%M:%S'), employee_code, customer_name,
             0, 0, 0, 0, 0)
        )

        # Thêm sản phẩm vào chi tiết hóa đơn
        for product_code, name_product, product_type, price in products:
            quantity = random.randint(1, 5)  # Random số lượng từ 1-5
            subtotal = quantity * price

            if product_type == "drink":
                total_quantity_drink += quantity
                total_price_drink += subtotal
            else:
                total_quantity_food += quantity
                total_price_food += subtotal

            total_price += subtotal

            cursor.execute(
                f"INSERT INTO {INVOICE_DETAIL_TABLE_NAME} ({INVOICE_DETAIL_INVOICE_CODE}, {INVOICE_DETAIL_PRODUCT_ID_BARCODE}, "
                f"{INVOICE_DETAIL_PRODUCT_NAME}, {INVOICE_DETAIL_PRODUCT_TYPE}, {INVOICE_DETAIL_QUANTITY}, "
                f"{INVOICE_DETAIL_PRICE}, {INVOICE_DETAIL_SUBTOTAL}, {INVOICE_DETAIL_CUSTOMER_NAME}) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (invoice_code, product_code, name_product, product_type, quantity, price, subtotal, customer_name)
            )

        # Cập nhật tổng số lượng và giá vào bảng Invoice
        cursor.execute(
            f"UPDATE {INVOICE_TABLE_NAME} SET {INVOICE_TOTAL_QUANTITY_DRINK}=?, {INVOICE_TOTAL_QUANTITY_FOOD}=?, "
            f"{INVOICE_TOTAL_PRICE_DRINK}=?, {INVOICE_TOTAL_PRICE_FOOD}=?, {INVOICE_TOTAL_PRICE}=? WHERE {INVOICE_CODE}=?",
            (total_quantity_drink, total_quantity_food, total_price_drink, total_price_food, total_price, invoice_code)
        )

        invoice_counter += 1

    start_date += delta

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()
print("✅ Dữ liệu hóa đơn đã được thêm đầy đủ và chính xác!")
