
import os

DEFAULT_TIME ="%Y-%m-%d %H:%M:%S"
PATH_CART = r"D:\BTL_Python_done1603\resource\cart.txt"
PATH_RECOGNIZE=r"D:\BTL_Python_done1603\resource\recognize.txt"
# Đặt tên file database
DATABASE_NAME = r"D:\BTL_Python_done1603\resource\food_management.db"

# Bảng Nhân viên
EMPLOYEE_TABLE_NAME = "Employee"
EMPLOYEE_ID = "id"  # Khóa chính
EMPLOYEE_CODE = "employee_code"  # Mã nhân viên (MNV)
EMPLOYEE_USERNAME = "username"  # Tên đăng nhập
EMPLOYEE_PASSWORD = "password"  # Mật khẩu
EMPLOYEE_ADDRESS = "address"  # Địa chỉ
EMPLOYEE_GENDER = "gender"  # Giới tính (Nam, Nữ, Khác)
EMPLOYEE_BIRTHDATE = "birthdate"  # Ngày sinh
EMPLOYEE_PHONE = "phone"  # Số điện thoại nhân viên
EMPLOYEE_ROLE = "role"  # Vai trò (admin, employee)

# Bảng Tài khoản nhân viên
ACCOUNT_EMPLOYEE_TABLE_NAME = "AccountEmployee"
ACCOUNT_EMPLOYEE_ID = "id"
ACCOUNT_EMPLOYEE_USERNAME = "username"  # Tên đăng nhập (Ma_NV)
ACCOUNT_EMPLOYEE_PASSWORD = "password"  # Mật khẩu
ACCOUNT_EMPLOYEE_ROLE = "role"  # Vai trò (admin, employee)





# Bảng Khách hàng
CUSTOMER_TABLE_NAME = "Customer"
CUSTOMER_ID = "id"
CUSTOMER_CODE = "customer_code"  # Ma_KH
CUSTOMER_NAME = "customer_name"  # Ten_KH
CUSTOMER_PHONE = "customer_phone"  # SDT_KH
CUSTOMER_POINT = "points"  # Diem

# Bảng Sản phẩm
PRODUCT_TABLE_NAME = "Product"
PRODUCT_ID = "id"
PRODUCT_CODE = "product_code"  # Ma_SP
PRODUCT_ID_BARCODE ="product_id_barcode"
PRODUCT_NAME = "product_name"  # Ten_SP
PRODUCT_PRICE = "price"  # Gia_SP
PRODUCT_STOCK = "stock"  # SoLuong_SP
PRODUCT_TYPE = "product_type"  # Loai_SP (drink, food)
PRODUCT_POINTS = "points"  # Diem_SP



# Bảng Hóa Đơn
INVOICE_TABLE_NAME = "Invoice"
INVOICE_ID = "id"
INVOICE_CODE = "invoice_code"  # Mã hóa đơn
INVOICE_EMPLOYEE_CODE = EMPLOYEE_CODE
INVOICE_DATE_CREATED = "date_created"  # Ngày tạo
INVOICE_CUSTOMER_NAME = CUSTOMER_NAME
INVOICE_TOTAL_QUANTITY_DRINK = "total_quantity_drink"  # Tổng số lượng nước
INVOICE_TOTAL_QUANTITY_FOOD = "total_quantity_food"  # Tổng số lượng đồ ăn
INVOICE_TOTAL_PRICE_DRINK = "total_price_drink"  # Tổng tiền nước
INVOICE_TOTAL_PRICE_FOOD = "total_price_food"  # Tổng tiền đồ ăn
INVOICE_TOTAL_PRICE = "total_price"  # Tổng tiền

# Bảng Chi Tiết Hóa Đơn
INVOICE_DETAIL_TABLE_NAME = "InvoiceDetail"
INVOICE_DETAIL_ID = "id"
INVOICE_DETAIL_INVOICE_CODE = INVOICE_CODE  # Mã hóa đơn
INVOICE_DETAIL_PRODUCT_ID_BARCODE = PRODUCT_ID_BARCODE
INVOICE_DETAIL_PRODUCT_NAME = PRODUCT_NAME
INVOICE_DETAIL_PRODUCT_TYPE = PRODUCT_TYPE
INVOICE_DETAIL_QUANTITY = "quantity"  # Số lượng
INVOICE_DETAIL_PRICE = "price"  # Đơn giá
INVOICE_DETAIL_SUBTOTAL = "subtotal"  # Thành tiền
INVOICE_DETAIL_CUSTOMER_NAME = CUSTOMER_NAME


# Bảng Báo cáo (Report)
REPORT_TABLE_NAME = "Report"
REPORT_ID = "id"
REPORT_CODE = "report_code"  # Mã báo cáo
REPORT_CREATE_AT = "create_at"  # Thời gian tạo báo cáo
REPORT_QUANTITY_DRINK = "quantity_drink"  # Số lượng đồ uống
REPORT_TOTAL_PRICE_DRINK = "total_price_drink"  # Tổng giá tiền đồ uống
REPORT_QUANTITY_FOOD = "quantity_food"  # Số lượng đồ ăn
REPORT_TOTAL_PRICE_FOOD = "total_price_food"  # Tổng giá tiền đồ ăn
REPORT_TOTAL_PRODUCT_SOLD = "total_product_sold"  # Tổng số sản phẩm bán ra
REPORT_TOTAL_PRICE = "total_price"  # Tổng giá tiền

# Mật khẩu mặc định cho tài khoản nhân viên
DEFAULT_PASSWORD = "123"

# Cấu hình môi trường
SECRET_KEY = os.getenv("SECRET_KEY", "my_secret_key")  # Key cho mã hóa nếu cần
