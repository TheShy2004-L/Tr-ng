import json
import os
import time
import tkinter as tk
from datetime import datetime
from time import sleep
from tkinter import ttk, messagebox
import threading

import cv2

from Entity.Invoice import Invoice

from config1.config import PATH_CART, PATH_RECOGNIZE, INVOICE_DETAIL_PRODUCT_NAME, INVOICE_DETAIL_QUANTITY, \
    INVOICE_DETAIL_PRICE, INVOICE_DETAIL_INVOICE_CODE, INVOICE_DETAIL_PRODUCT_TYPE
from controllers.invoice_controller import InvoiceController
from controllers.invoice_detail_controller import InvoiceDetailController
from controllers.thread import ThreadController
from models.invoice_model import InvoiceModel


def take_info_cart():
    try:
        with open(PATH_CART, "r") as file:
            return json.load(file)  # ✅ Đọc toàn bộ danh sách JSON
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Lỗi đọc giỏ hàng từ file trong VIEW: {e}")
        return []  # Trả về danh sách rỗng nếu lỗi



class InvoiceOrderView:
    def __init__(self, parent):
        self.root = parent  # Đối tượng Tk chính
        self.root.title("Invoice Management System")
        self.root.geometry("1980x1080")  # Kích thước cửa sổ mặc định
        self.invoice_detail_controller = InvoiceDetailController()
        self.invoice_controller = InvoiceController()
        self.cart = []  # Giỏ hàng (danh sách các sản phẩm đã chọn)
        self.create_widgets()
        self.product_list.bind("<ButtonRelease-1>", self.on_row_selected)
        self.thread = ThreadController()
        self.thread.start_scanning()


        thread = threading.Thread(target=self.confim_change, daemon=True)
        thread.start()

    def confim_change(self):
        while True:
            with open(PATH_RECOGNIZE, "r") as file:
                if file.read() == "True" :
                    self.cart = take_info_cart()
                    for i in self.cart:
                        self.add_product_to_cart(i[INVOICE_DETAIL_PRODUCT_NAME],
                                                 i[INVOICE_DETAIL_QUANTITY],
                                                 i[INVOICE_DETAIL_PRICE])
            sleep(0.2)

    def create_widgets(self):
        # Chia giao diện thành 2 cột (có tỉ lệ bằng nhau)
        self.root.grid_columnconfigure(0, weight=1, uniform="equal")
        self.root.grid_columnconfigure(1, weight=1, uniform="equal")
        self.root.grid_rowconfigure(0, weight=1)

        # Left Frame (Giỏ hàng)
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Right Frame (Hóa đơn)
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Label quét mã sản phẩm
        self.scan_label = ttk.Label(self.left_frame, text="Giỏ hàng", font=("Arial", 14))
        self.scan_label.grid(row=0, column=0, pady=10)



        # Danh sách sản phẩm
        self.product_list = ttk.Treeview(self.left_frame, columns=("Tên sản phẩm", "Số lượng", "Giá"), show="headings", height=10)
        self.product_list.heading("Tên sản phẩm", text="Tên sản phẩm")
        self.product_list.heading("Số lượng", text="Số lượng")
        self.product_list.heading("Giá", text="Giá")
        self.product_list.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        # Nút Xác nhận để hiển thị hóa đơn
        self.confirm_button = ttk.Button(self.left_frame, text="Xác nhận", command=self.show_invoice)
        self.confirm_button.grid(row=3, column=0, padx=5, pady=10)

        # Cấu hình để các cột và hàng có thể co giãn
        self.left_frame.grid_rowconfigure(0, weight=0)
        self.left_frame.grid_rowconfigure(1, weight=0)
        self.left_frame.grid_rowconfigure(2, weight=1)  # Bảng sản phẩm có thể giãn ra
        self.left_frame.grid_rowconfigure(3, weight=0)

        # Bên phải (hiển thị hóa đơn)
        self.invoice_label = ttk.Label(self.right_frame, text="Hóa đơn", font=("Arial", 14))
        self.invoice_label.grid(row=0, column=0, pady=10)

        self.invoice_text = tk.Text(self.right_frame, width=40, height=15, wrap=tk.WORD, font=("Arial", 12))
        self.invoice_text.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.right_frame.grid_columnconfigure(0, weight=1)  # Căn giữa theo chiều ngang
        self.right_frame.grid_rowconfigure(1, weight=1)  # Căn giữa theo chiều dọc
        # Nút "Xuất Bill"
        # Thay đổi trong create_widgets()
        self.print_button = ttk.Button(self.right_frame, text="Xuất Bill",
                                       command=lambda: threading.Thread(target=self.export_bill, daemon=True).start())
        self.print_button.grid(row=2, column=0, pady=10)

        # Cấu hình để các cột và hàng có thể co giãn
        self.right_frame.grid_rowconfigure(0, weight=0)
        self.right_frame.grid_rowconfigure(1, weight=1)  # Hóa đơn có thể giãn ra
        self.right_frame.grid_rowconfigure(2, weight=0)

        # Cấu hình cột cho các frame
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)



    def add_product_to_cart(self, product_name, quantity, price):

        for item in self.cart:
            if item[INVOICE_DETAIL_PRODUCT_NAME] == product_name:
                item[INVOICE_DETAIL_QUANTITY] = quantity
                item[INVOICE_DETAIL_PRICE] = item[INVOICE_DETAIL_QUANTITY] * price
                self.update_product_list()
                return
        self.update_product_list()

    def update_product_list(self):
        # Xóa toàn bộ dữ liệu cũ trong `Treeview`
        for item2 in self.product_list.get_children():
            self.product_list.delete(item2)

        # Thêm dữ liệu mới từ `self.cart`
        for item in self.cart:
            self.product_list.insert("", "end", values=(item["product_name"], item["quantity"], item["price"]))

    def show_invoice(self):
        """Hiển thị hóa đơn và căn giữa trong Frame."""
        self.invoice_text.delete(1.0, tk.END)  # Xóa nội dung cũ

        if not self.cart:
            self.invoice_text.insert(tk.END, "Giỏ hàng trống!\n")
            return

        total_price = 0
        width = 40  # Chiều rộng nội dung hóa đơn

        invoice_content = " HÓA ĐƠN ".center(width, "=") + "\n"
        invoice_content += "{:<20} {:<8} {:<12}\n".format("Tên sản phẩm", "SL", "Thành tiền").center(width)
        invoice_content += "-" * width + "\n"

        for item in self.cart:
            name = item[INVOICE_DETAIL_PRODUCT_NAME]
            quantity = item[INVOICE_DETAIL_QUANTITY]
            price = item[INVOICE_DETAIL_PRICE]
            total_price += price  # Cộng dồn tổng tiền

            invoice_content += "{:<20} {:<8} {:<12,}\n".format(name, quantity, price).center(width)

        invoice_content += "-" * width + "\n"
        invoice_content += f"{'Tổng tiền:':<20} {total_price:,} VND".center(width) + "\n"

        self.invoice_text.insert(tk.END, invoice_content)  # Hiển thị hóa đơn

        self.save_bill_in_db()

    def export_bill(self):
        """Lưu hóa đơn vào file .txt và làm mới giao diện"""
        content = self.invoice_text.get("1.0", "end-1c")
        now = datetime.now().strftime("%Y%m%d_%H%M%S")  # Tạo mã thời gian
        folder_path = r"D:\Main\resource\Invoice"  # Đường dẫn thư mục
        file_name = f"{now}.txt"
        file_path = os.path.join(folder_path, file_name)

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

            # Hiển thị thông báo trên luồng chính (Tránh lỗi giao diện bị đứng)
            self.root.after(0, lambda: messagebox.showinfo("Thành công", f"Hóa đơn đã được lưu: {file_path}"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi khi lưu hóa đơn: {e}"))

        # Làm mới giao diện trên luồng chính
        self.root.after(0, self.reset_invoice_ui)

    def reset_invoice_ui(self):
        """Xóa nội dung hóa đơn và giỏ hàng sau khi xuất bill"""
        try:
            self.invoice_text.delete("1.0", "end")
            for item in self.product_list.get_children():
                self.product_list.delete(item)

            # Dừng và khởi động lại quá trình quét
            self.thread.stop_scanning()
            self.thread = ThreadController()
            self.thread.start_scanning()
        except Exception as e:
            print("Lỗi khi làm mới hóa đơn:", str(e))

    def save_bill_in_db(self):
        food_quantity = 0
        drink_quantity = 0
        total_price_food = 0
        total_price_drink = 0
        invoice_code =""
        for item in self.cart:
            invoice_code = item[INVOICE_DETAIL_INVOICE_CODE]
            print(item)
            self.invoice_detail_controller.add_invoice_detail(**item)
            if item[INVOICE_DETAIL_PRODUCT_TYPE] == "drink":
                drink_quantity += item[INVOICE_DETAIL_QUANTITY]
                total_price_drink +=item[INVOICE_DETAIL_PRICE]
            if item[INVOICE_DETAIL_PRODUCT_TYPE] == "food":
                food_quantity+= item[INVOICE_DETAIL_QUANTITY]
                total_price_food+=item[INVOICE_DETAIL_PRICE]
        total_price = int(total_price_food) + int(total_price_drink)
        invoice = Invoice("NV001","khách lẻ",drink_quantity,
                          food_quantity,total_price_drink,total_price_food,total_price,invoice_code)
        self.invoice_controller.update_invoice_scan(invoice)





#     đây là hàm khi án vào có quyền sửa
    def on_row_selected(self, event):
        selected_item = self.product_list.focus()  # Lấy ID của hàng được chọn
        values = self.product_list.item(selected_item, 'values')  # Lấy dữ liệu hàng
        if not values:
            return

        # Mở cửa sổ popup chỉnh sửa
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Chỉnh sửa sản phẩm")
        edit_window.geometry("300x200")

        ttk.Label(edit_window, text="Tên sản phẩm:").pack(pady=5)
        name_label = ttk.Label(edit_window, text=values[0])  # Hiển thị tên sản phẩm
        name_label.pack()

        ttk.Label(edit_window, text="Số lượng mới:").pack(pady=5)
        quantity_entry = ttk.Entry(edit_window)
        quantity_entry.insert(0, values[1])  # Điền số lượng cũ vào
        quantity_entry.pack()

        def update_product():
            new_quantity = quantity_entry.get()
            if not new_quantity.isdigit() or int(new_quantity) < 0:
                messagebox.showerror("Lỗi", "Số lượng không hợp lệ!")
                return

            new_quantity = int(new_quantity)
            if new_quantity == 0:
                self.remove_product(values[0])  # Xóa sản phẩm nếu số lượng = 0
            else:
                self.update_quantity(values[0], new_quantity)

            edit_window.destroy()  # Đóng cửa sổ chỉnh sửa


        def delete_product():
            self.remove_product(values[0])
            edit_window.destroy()

        ttk.Button(edit_window, text="Cập nhật", command=update_product).pack(pady=5)
        ttk.Button(edit_window, text="Xóa", command=delete_product).pack(pady=5)
        ttk.Button(edit_window, text="Hủy", command=edit_window.destroy).pack(pady=5)

    def update_quantity(self, product_name, new_quantity):
        for item in self.cart:
            if item[INVOICE_DETAIL_PRODUCT_NAME] == product_name:
                item[INVOICE_DETAIL_QUANTITY] = new_quantity
                item[INVOICE_DETAIL_PRICE] = new_quantity * (
                            item[INVOICE_DETAIL_PRICE] / int(self.product_list.item(self.product_list.focus(), 'values')[1]))
                break
        self.update_product_list()

    def remove_product(self, product_name):
        self.cart = [item for item in self.cart if item[INVOICE_DETAIL_PRODUCT_NAME] != product_name]
        self.update_product_list()
