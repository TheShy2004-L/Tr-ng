import tkinter as tk
import time

from view.invoice_view.invoice_order_view import InvoiceOrderView


class MainApp:
    def __init__(self, parent):
        self.app = None
        self.new_window = None
        self.root = parent
        self.root.title("Hệ Thống Quản Lý")
        self.root.state("zoomed")  # Toàn màn hình
        self.root.configure(bg="#E3F2FD")  # Màu nền sáng

        # Frame chính
        self.main_frame = tk.Frame(self.root, bg="#E3F2FD")
        self.main_frame.pack(expand=True, fill="both")

        # Hiển thị ngày tháng & đồng hồ
        self.time_label = tk.Label(self.main_frame, font=("Arial", 18, "bold"), bg="#E3F2FD", fg="#1976D2")
        self.time_label.pack(pady=20)
        self.update_time()

        # Tạo frame chứa các nút
        self.button_frame = tk.Frame(self.main_frame, bg="#E3F2FD")
        self.button_frame.pack(expand=True)

        # Nút Order
        self.order_btn = tk.Button(
            self.button_frame, text="📦 Order", width=20, height=3, bg="#4CAF50", fg="white",
            font=("Arial", 14, "bold"), relief="raised", borderwidth=5, command=self.open_order
        )
        self.order_btn.grid(row=0, column=0, padx=20, pady=20, ipadx=10, ipady=10)

        # Nút Management
        self.mgmt_btn = tk.Button(
            self.button_frame, text="⚙️ Management", width=20, height=3, bg="#2196F3", fg="white",
            font=("Arial", 14, "bold"), relief="raised", borderwidth=5, command=self.open_management
        )
        self.mgmt_btn.grid(row=0, column=1, padx=20, pady=20, ipadx=10, ipady=10)

    def update_time(self):
        """Cập nhật thời gian liên tục"""
        current_time = time.strftime("%d/%m/%Y %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def open_order(self):
        self.root.withdraw()
        self.new_window = tk.Toplevel(self.root)
        self.app = InvoiceOrderView(self.new_window)

        def on_close():
            """Khi đóng cửa sổ mới, hiển thị lại cửa sổ chính"""
            self.root.deiconify()
            self.new_window.destroy()

        self.new_window.protocol("WM_DELETE_WINDOW", on_close)

    def open_management(self):
        self.root.withdraw()
        self.new_window = tk.Toplevel(self.root)
        from view.main_view.admin_view import AdminDashboard
        self.app = AdminDashboard(self.new_window)

        def on_close():
            """Khi đóng cửa sổ mới, hiển thị lại cửa sổ chính"""
            self.root.deiconify()
            self.new_window.destroy()

        self.new_window.protocol("WM_DELETE_WINDOW", on_close)