import calendar
import tkinter as tk
from datetime import datetime
from tkinter import ttk


from config1.config import INVOICE_DETAIL_ID, INVOICE_EMPLOYEE_CODE, INVOICE_DATE_CREATED, INVOICE_CUSTOMER_NAME, \
    INVOICE_TOTAL_QUANTITY_DRINK, INVOICE_TOTAL_QUANTITY_FOOD, INVOICE_TOTAL_PRICE_DRINK, INVOICE_TOTAL_PRICE_FOOD, \
    INVOICE_TOTAL_PRICE, INVOICE_CODE, INVOICE_DETAIL_CUSTOMER_NAME, INVOICE_DETAIL_PRODUCT_ID_BARCODE, \
    INVOICE_DETAIL_PRODUCT_NAME, INVOICE_DETAIL_INVOICE_CODE, INVOICE_DETAIL_PRODUCT_TYPE, INVOICE_DETAIL_QUANTITY, \
    INVOICE_DETAIL_PRICE, INVOICE_DETAIL_SUBTOTAL
from controllers.invoice_controller import InvoiceController
from controllers.invoice_detail_controller import InvoiceDetailController


class InvoiceTableView(tk.Frame):  # Kế thừa tk.Frame
    def __init__(self, parent):
        super().__init__(parent)  # Gọi constructor của tk.Frame
        self.invoice_controller = InvoiceController()
        self.invoice_detail_controller = InvoiceDetailController()

        self.pack(fill="both", expand=True)  # Để hiển thị đầy đủ khi gọi từ AdminDashboard
        self.selected_date()
        self.create_invoice_view()
        self.create_invoice_detail_view()
        self.load_invoice_data()

    def selected_date(self):
        self.combo_frame = ttk.Frame(self)
        self.combo_frame.pack(pady=10)

        self.year_label = ttk.Label(self.combo_frame, text="Chọn năm:", font=("Arial", 12))
        self.year_label.grid(row=0, column=0, padx=5)
        self.year_combobox = ttk.Combobox(self.combo_frame, font=("Arial", 12), state="readonly", width=5)
        self.year_combobox.grid(row=0, column=1, padx=5)

        self.month_label = ttk.Label(self.combo_frame, text="Chọn tháng:", font=("Arial", 12))
        self.month_label.grid(row=0, column=2, padx=5)
        self.month_combobox = ttk.Combobox(self.combo_frame, font=("Arial", 12), state="readonly", width=3)
        self.month_combobox.grid(row=0, column=3, padx=5)

        self.date_label = ttk.Label(self.combo_frame, text="Chọn ngày:", font=("Arial", 12))
        self.date_label.grid(row=0, column=4, padx=5)
        self.date_combobox = ttk.Combobox(self.combo_frame, font=("Arial", 12), state="readonly", width=3)
        self.date_combobox.grid(row=0, column=5, padx=5)

        self.search_button = ttk.Button(self.combo_frame, text="🔍 Tìm kiếm", command=self.search_invoice)
        self.search_button.grid(row=0, column=6, padx=10)

        self.update_year_options()
        self.update_month_options()
        self.year_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_date_options())
        self.month_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_date_options())
        self.update_date_options()

    def search_invoice(self):
        selected_year = self.year_combobox.get()
        selected_month = self.month_combobox.get()
        selected_day = self.date_combobox.get()
        if selected_year and selected_month and selected_day:
            for item in self.invoice_tree.get_children():
                self.invoice_tree.delete(item)
            for item in self.detail_tree.get_children():
                self.detail_tree.delete(item)
            invoices = self.invoice_controller.get_invoice_by_day(selected_day, selected_month, selected_year)
            for invoice in invoices:
                self.invoice_tree.insert("", "end", values=invoice)

    def update_year_options(self):
        current_year = datetime.now().year
        self.year_combobox["values"] = [str(year) for year in range(2020, 2031)]
        self.year_combobox.set(str(current_year))

    def update_month_options(self):
        self.month_combobox["values"] = [f"{month:02d}" for month in range(1, 13)]
        self.month_combobox.set(f"{datetime.now().month:02d}")

    def update_date_options(self):
        try:
            year, month = int(self.year_combobox.get()), int(self.month_combobox.get())
            self.date_combobox["values"] = [f"{day:02d}" for day in range(1, calendar.monthrange(year, month)[1] + 1)]
            self.date_combobox.set(f"{calendar.monthrange(year, month)[1]:02d}")
        except ValueError:
            pass

    def create_invoice_view(self):
        title_frame = tk.Frame(self, bg="#007bff", padx=10, pady=10)
        title_frame.pack(fill="x")
        tk.Label(title_frame, text="QUẢN LÝ HÓA ĐƠN", fg="white", bg="#007bff", font=("Arial", 16, "bold")).pack()
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        style.configure("Treeview.Heading", font=("Tahoma", 10), background="#007bff",
                        foreground="black")  # Đổi chữ thành màu đen
        table_frame = tk.Frame(self, bg="#f8f9fa", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        columns = [INVOICE_EMPLOYEE_CODE, INVOICE_DATE_CREATED, INVOICE_CUSTOMER_NAME, INVOICE_TOTAL_QUANTITY_DRINK,
                   INVOICE_TOTAL_QUANTITY_FOOD, INVOICE_TOTAL_PRICE_DRINK, INVOICE_TOTAL_PRICE_FOOD,
                   INVOICE_TOTAL_PRICE, INVOICE_CODE]
        self.invoice_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.invoice_tree.heading(col, text=col.replace("_", " "))
            self.invoice_tree.column(col, width=120)
        self.invoice_tree.pack(fill="both", expand=True)
        self.invoice_tree.bind("<<TreeviewSelect>>", self.on_invoice_selected)

    def create_invoice_detail_view(self):
        detail_frame = tk.Frame(self, bg="#f8f9fa", padx=10, pady=10)
        detail_frame.pack(fill="both", expand=True)
        tk.Label(detail_frame, text="CHI TIẾT HÓA ĐƠN", font=("Arial", 14, "bold"), bg="#f8f9fa").pack()
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        style.configure("Treeview.Heading", font=("Tahoma", 10), background="#007bff",
                        foreground="black")  # Đổi chữ thành màu đen
        columns = [INVOICE_DETAIL_ID, INVOICE_DETAIL_INVOICE_CODE, INVOICE_DETAIL_PRODUCT_NAME,
                   INVOICE_DETAIL_PRODUCT_TYPE, INVOICE_DETAIL_QUANTITY, INVOICE_DETAIL_PRICE,
                   INVOICE_DETAIL_SUBTOTAL, INVOICE_DETAIL_CUSTOMER_NAME, INVOICE_DETAIL_PRODUCT_ID_BARCODE]
        self.detail_tree = ttk.Treeview(detail_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.detail_tree.heading(col, text=col.replace("_", " "))
            self.detail_tree.column(col, width=120)
        self.detail_tree.pack(fill="both", expand=True)

    def load_invoice_data(self):
        invoices = self.invoice_controller.get_all_invoice()
        for invoice in invoices:
            self.invoice_tree.insert("", "end", values=invoice)

    def on_invoice_selected(self, event):
        selected_item = self.invoice_tree.selection()
        if selected_item:
            row_data = self.invoice_tree.item(selected_item[0], "values")
            invoice_code = row_data[8]
            self.load_invoice_detail_data(invoice_code)

    def load_invoice_detail_data(self, invoice_code):
        for item in self.detail_tree.get_children():
            self.detail_tree.delete(item)
        list_detail = self.invoice_detail_controller.get_all_by_invoice_code(invoice_code)
        for detail in list_detail:
            self.detail_tree.insert("", "end", values=detail)
