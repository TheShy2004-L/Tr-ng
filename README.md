# HỆ THỐNG QUẢN LÝ CỬA HÀNG BÁN ĐỒ ĂN VẶT

## Giới thiệu

Đây là một phần mềm quản lý dành cho **các cửa hàng bán đồ ăn vặt**, giúp số hoá quy trình kinh doanh với các chức năng như: quản lý sản phẩm, đơn hàng, khách hàng, nhân viên, và hỗ trợ quét mã QR hóa đơn. Hệ thống có giao diện trực quan được xây dựng bằng Tkinter, sử dụng cơ sở dữ liệu SQLite và tích hợp thư viện OpenCV – Pyzbar để xử lý mã vạch/mã QR.
## Công nghệ sử dụng
-  **Ngôn ngữ lập trình:** Python 3.x  
-  **Giao diện người dùng:** Tkinter  
-  **Cơ sở dữ liệu:** SQLite3  
-  **Xử lý mã QR:** OpenCV + Pyzbar  
-  **Mô hình phát triển:** MVC (Model - View - Controller)  
## Các chức năng chính

 **Quản lý sản phẩm**
  - Thêm/sửa/xoá món ăn, đồ uống
  - Hiển thị tồn kho, giá bán, phân loại món

 **Quản lý đơn hàng**
  - Tạo đơn hàng theo thời gian thực
  - Tính tổng tiền, in hóa đơn
  - Quét mã QR để truy xuất đơn hàng

 **Quản lý khách hàng**
  - Lưu thông tin khách hàng
  - Tra cứu lịch sử mua hàng

 **Quản lý nhân viên**
  - Thêm/sửa thông tin nhân viên
  - Phân quyền truy cập

**Thống kê - báo cáo**
  - Doanh thu theo ngày/tháng
  - Món bán chạy nhất
  - Biểu đồ hóa đơn & sản phẩm
