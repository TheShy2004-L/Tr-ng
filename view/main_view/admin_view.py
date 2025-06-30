import os
import sys
from tkinter import messagebox
import tkinter as tk

from view.customer_view.customer_view import CustomerView
from view.employee_view.EmployeeView import EmployeeView
from view.invoice_view.invoice_table_view import InvoiceTableView
from view.main_view.login_view import LoginView
from view.product_view.product_view import ProductView
from view.report_view.ReportTable.report_view_and_chart import ReportViewAndChart


class AdminDashboard(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Management Dashboard")
        self.root.state("zoomed")
        self.root.configure(bg="#F5F7FA")

        # Sidebar menu
        self.sidebar = tk.Frame(self.root, bg="#1976D2", width=250)
        self.sidebar.pack(side="left", fill="y")

        self.title_label = tk.Label(
            self.sidebar, text="📌 MENU", font=("Arial", 18, "bold"), fg="white", bg="#1976D2"
        )
        self.title_label.pack(pady=20)

        self.buttons = [
            ("👥 Employee Management", EmployeeView),
            ("📞 Customer Management", CustomerView),
            ("📦 Product Management", ProductView),
            ("🧾 Invoice Management", InvoiceTableView),
            ("📊 Report Management", ReportViewAndChart),
        ]

        for text, view_class in self.buttons:
            btn = tk.Button(
                self.sidebar, text=text, command=lambda v=view_class: self.open_view(v),
                bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
                width=25, height=2, relief="flat", borderwidth=2, activebackground="#1565C0"
            )
            btn.pack(pady=5, padx=10, fill="x")



        # Nút Đăng xuất
        self.logout_button = tk.Button(
            self.sidebar, text="🚪 Logout", command=self.logout,
            bg="#D32F2F", fg="white", font=("Arial", 12, "bold"),
            width=20, height=2, relief="flat", activebackground="#B71C1C"
        )
        self.logout_button.pack(pady=20, padx=10, fill="x")

        # Khu vực nội dung hiển thị
        self.content_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Thêm thông báo chào mừng
        self.welcome_label = tk.Label(
            self.content_frame, text="Welcome to Management Dashboard!", font=("Arial", 20, "bold"),
            fg="#333333", bg="white"
        )
        self.welcome_label.pack(pady=20)

    def open_view(self, view_class):
        """Hiển thị giao diện tương ứng bên phải"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()  # Xóa nội dung cũ

        view = view_class(self.content_frame)  # Khởi tạo view trong content_frame
        view.pack(fill="both", expand=True)  # Để view hiển thị đầy đủ

    def logout(self):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?")
        if confirm:
            with open(r"D:\BTL_Python_done1603\resource\user.txt", "w") as file:
                file.write(f"None")
            self.root.destroy()
            new_root = tk.Tk()
            LoginView(new_root)
            new_root.mainloop()



