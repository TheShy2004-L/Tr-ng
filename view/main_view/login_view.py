import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from controllers.employee_controller import EmployeeController
from models.employe_model import EmployeeModel
from view.main_view.home import MainApp


class LoginView:
    def __init__(self, parent):
        self.model_employee = EmployeeModel()
        self.root = parent
        self.root.title("Quản lý cửa hàng đồ ăn vặt")
        self.root.geometry("400x350")
        self.root.configure(bg="#f5f5f5")  # Màu nền nhẹ hơn

        # Tiêu đề
        ttk.Label(self.root, text="Cửa hàng Ăn Vặt Vali Ve Nua", font=("Segoe UI", 18, "bold"),
                  foreground="#007ACC", background="#f5f5f5").pack(pady=15)

        # Frame chứa ô nhập liệu
        frame = ttk.Frame(self.root, padding=15)
        frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(frame, text="Tên đăng nhập:", font=("Segoe UI", 12), background="#f5f5f5").pack(anchor="w", pady=5)
        self.entry_username = ttk.Entry(frame, font=("Segoe UI", 12))
        self.entry_username.pack(fill="x", pady=5, padx=5)

        ttk.Label(frame, text="Mật khẩu:", font=("Segoe UI", 12), background="#f5f5f5").pack(anchor="w", pady=5)
        self.entry_password = ttk.Entry(frame, show="*", font=("Segoe UI", 12))
        self.entry_password.pack(fill="x", pady=5, padx=5)

        # Nút đăng nhập
        self.login_button = ttk.Button(self.root, text="Đăng nhập", command=self.verify_account, style="TButton")
        self.login_button.pack(pady=20)

        # Thiết lập style
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 12), padding=8, background="#5cb85c", foreground="black")
        style.map("TButton", background=[("active", "#4cae4c")])  # Nhấn vào có màu nhẹ hơn

    def get_login_info(self):
        """Lấy thông tin đăng nhập"""
        return self.entry_username.get(), self.entry_password.get()

    def verify_account(self):
        user = self.model_employee.login(*self.get_login_info())
        if user:
            with open(r"D:\BTL_Python_done1603\resource\user.txt", "w") as file:
                file.write(f"{user[2]},{user[8]}")  # Lưu username vào file
            self.root.destroy()  # Đóng cửa sổ đăng nhập
            root_main = tk.Tk()
            MainApp(root_main)  # Mở cửa sổ chính
            root_main.mainloop()
        else:
            self.show_error("Login", "Username or password incorrect")

    def show_message(self, title, message):
        """Hiển thị thông báo"""
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        """Hiển thị lỗi"""
        messagebox.showerror(title, message)


