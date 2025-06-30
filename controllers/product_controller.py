import tkinter as tk
from tkinter import ttk, messagebox
from models.product_model import ProductModel
from test_code import scan
from test_code.scan import ScanBarcode


class ProductController:

    def __init__(self, view):
        self.last_scanned_controller = None
        self.cre_scan = None
        self.product_info = None
        self.view = view  # Nhận view từ ProductView
        self.model = ProductModel()

        self.view.buttons["Scan to add"].config(command=self.open_cam_scan)
        self.view.buttons["Thêm"].config(command=self.add_product)
        self.view.buttons["Cập nhật"].config(command=self.update_product)
        self.view.buttons["Xóa"].config(command=self.delete_product)
        self.view.buttons["Làm mới"].config(command=self.load_products)
        self.view.search_button.config(command=self.search_product)
        self.view.tree.bind("<ButtonRelease-1>", self.select_product)

        self.model.connect_db()

    def load_products(self):
        rows = self.model.get_all_products()
        self.load_tree(rows)

    def load_tree(self, rows):
        self.view.tree.delete(*self.view.tree.get_children())
        for row in rows:
            self.view.tree.insert("", tk.END, values=row)

    def open_cam_scan(self):
        self.cre_scan = ScanBarcode()
        self.cre_scan.start_add_scanning()


    def add_product(self):
        data = {key: entry.get() for key, entry in self.view.entries.items()}
        if all(data.values()):
            self.model.add_product(data["Tên SP"], data["Giá"], data["Số lượng"], data["Loại"], data["Điểm thưởng"])
            self.load_products()
            messagebox.showinfo("Thành công", "Thêm sản phẩm thành công!")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin")

    def update_product(self):
        selected_item = self.view.tree.selection()
        if selected_item:
            item_values = self.view.tree.item(selected_item[0], "values")
            product_id = item_values[0]
            data = {key: entry.get() for key, entry in self.view.entries.items()}
            self.model.update_product(product_id, data["Tên SP"], data["Giá"], data["Số lượng"], data["Loại"], data["Điểm thưởng"])
            self.load_products()
            messagebox.showinfo("Thành công", "Cập nhật sản phẩm thành công!")

    def delete_product(self):
        selected_item = self.view.tree.selection()
        if selected_item:
            item_values = self.view.tree.item(selected_item[0], "values")
            product_id = item_values[0]
            self.model.delete_product(product_id)
            self.load_products()
            messagebox.showinfo("Thành công", "Xóa sản phẩm thành công!")

    def search_product(self):
        query = self.view.search_entry.get()
        rows = self.model.search_product(query)
        self.load_tree(rows)

    def select_product(self, event):
        selected_item = self.view.tree.selection()
        if selected_item:
            item_values = self.view.tree.item(selected_item[0], "values")
            self.view.entries["Tên SP"].delete(0, tk.END)
            self.view.entries["Tên SP"].insert(0, item_values[2])
            self.view.entries["Giá"].delete(0, tk.END)
            self.view.entries["Giá"].insert(0, item_values[3])
            self.view.entries["Số lượng"].delete(0, tk.END)
            self.view.entries["Số lượng"].insert(0, item_values[4])
            self.view.entries["Loại"].set(item_values[5])
            self.view.entries["Điểm thưởng"].delete(0, tk.END)
            self.view.entries["Điểm thưởng"].insert(0, item_values[6])
