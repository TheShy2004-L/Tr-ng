from tkinter import ttk, messagebox
import tkinter as tk

from config1.config import REPORT_ID, REPORT_CODE, REPORT_CREATE_AT, REPORT_QUANTITY_DRINK, REPORT_TOTAL_PRICE_DRINK, \
    REPORT_TOTAL_PRODUCT_SOLD, REPORT_QUANTITY_FOOD, REPORT_TOTAL_PRICE_FOOD, REPORT_TOTAL_PRICE
from controllers.report_controller import ReportController


class ReportView(tk.Frame):  # Kế thừa từ tk.Frame
    def __init__(self, parent):
        super().__init__(parent)  # Gọi constructor của tk.Frame
        self.root = parent  # Lưu tham chiếu đến cửa sổ cha
        self.pack(fill="both", expand=True)  # Để hiển thị đầy đủ
        self.report_controller = ReportController()
        self.row_data = None

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Tiêu đề
        title_frame = tk.Frame(self, bg="#007bff", padx=10, pady=10)
        title_frame.pack(fill="x")

        title_label = tk.Label(title_frame, text="BÁO CÁO DOANH THU", fg="white", bg="#007bff",
                               font=("Arial", 16, "bold"))
        title_label.pack()

        # Khu vực bảng
        table_frame = tk.Frame(self, bg="#f8f9fa", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        self.columns = [
            REPORT_ID, REPORT_CODE, REPORT_CREATE_AT,
            REPORT_QUANTITY_DRINK, REPORT_TOTAL_PRICE_DRINK,
            REPORT_QUANTITY_FOOD, REPORT_TOTAL_PRICE_FOOD,
            REPORT_TOTAL_PRODUCT_SOLD, REPORT_TOTAL_PRICE
        ]

        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings", height=15)
        column_headers = {
            REPORT_ID: "ID",
            REPORT_CODE: "Report Code",
            REPORT_CREATE_AT: "Date Created",
            REPORT_QUANTITY_DRINK: "Drink Quantity",
            REPORT_TOTAL_PRICE_DRINK: "Drink Price",
            REPORT_QUANTITY_FOOD: "Food Quantity",
            REPORT_TOTAL_PRICE_FOOD: "Food Price",
            REPORT_TOTAL_PRODUCT_SOLD: "Total Sold",
            REPORT_TOTAL_PRICE: "Total Price"
        }
        for col in self.columns:
            self.tree.heading(col, text=column_headers[col])
            self.tree.column(col, width=120, anchor="center")

        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        style.configure("Treeview.Heading", font=("Tahoma", 10), background="#007bff",
                        foreground="black")  # Đổi chữ thành màu đen

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_report_selected)

        # Khu vực nút chức năng
        button_frame = tk.Frame(self, bg="#f8f9fa", padx=10, pady=10)
        button_frame.pack(fill="x")

        self.update_button = tk.Button(button_frame, text="Cập nhật dữ liệu", font=("Arial", 12), bg="#28a745",
                                       fg="white",
                                       padx=10, command=self.update_report)
        self.update_button.pack(side=tk.LEFT, padx=10, pady=5)

    def on_report_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.row_data = self.tree.item(selected_item[0], "values")

    def update_report(self):
        self.report_controller.update_all_report()
        self.load_data()
        messagebox.showinfo("Thành công", "Dữ liệu đã được cập nhật thành công!")

    def load_data(self):
        self.tree.delete(*self.tree.get_children())  # Xóa dữ liệu cũ
        list_report = self.report_controller.get_reports()
        for item in list_report:
            self.tree.insert("", "end", values=item)