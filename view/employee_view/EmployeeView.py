import tkinter as tk
from tkinter import ttk

from config1.config import EMPLOYEE_CODE, EMPLOYEE_USERNAME, EMPLOYEE_PASSWORD, EMPLOYEE_ADDRESS, EMPLOYEE_GENDER, \
    EMPLOYEE_BIRTHDATE, EMPLOYEE_PHONE, EMPLOYEE_ROLE
from controllers.employee_controller import EmployeeController


class EmployeeView(tk.Frame):  # Kế thừa từ tk.Frame
    def __init__(self, parent):
        super().__init__(parent, bg="#f4f4f4")  # Nền sáng
        self.root = parent  # Lưu tham chiếu đến cửa sổ cha

        self.pack(fill="both", expand=True, padx=10, pady=10)  # Thêm padding để đẹp hơn
        self.setup_ui()
        self.controller = EmployeeController(self)

    def setup_ui(self):
        # Tiêu đề
        title_label = tk.Label(self, text="Quản lý Nhân viên", font=("Arial", 18, "bold"), fg="#333", bg="#f4f4f4")
        title_label.pack(pady=10)

        frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        frame.pack(pady=5, fill=tk.X)

        labels = [EMPLOYEE_CODE, EMPLOYEE_USERNAME, EMPLOYEE_PASSWORD, EMPLOYEE_ADDRESS, EMPLOYEE_GENDER,
                  EMPLOYEE_BIRTHDATE, EMPLOYEE_PHONE, EMPLOYEE_ROLE]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(frame, text=label, font=("Arial", 10, "bold"), bg="#ffffff").grid(row=0, column=i, padx=5, pady=3)
            entry = tk.Entry(frame, width=15, font=("Arial", 10)) if label != EMPLOYEE_GENDER else ttk.Combobox(frame,
                                                                                                                values=[
                                                                                                                    "Nam",
                                                                                                                    "Nữ",
                                                                                                                    "Khác"],
                                                                                                                state="readonly",
                                                                                                                width=12)
            entry.grid(row=1, column=i, padx=5, pady=3)
            self.entries[label] = entry

        button_frame = tk.Frame(self, bg="#f4f4f4")
        button_frame.pack(pady=10)

        self.buttons = {
            "Thêm": tk.Button(button_frame, text="Thêm", width=10, bg="#28a745", fg="white",
                              font=("Arial", 10, "bold")),
            "Sửa": tk.Button(button_frame, text="Sửa", width=10, bg="#007bff", fg="white", font=("Arial", 10, "bold")),
            "Xóa": tk.Button(button_frame, text="Xóa", width=10, bg="#dc3545", fg="white", font=("Arial", 10, "bold")),
            "Làm mới": tk.Button(button_frame, text="Làm mới", width=10, bg="#6c757d", fg="white",
                                 font=("Arial", 10, "bold"))
        }
        for btn in self.buttons.values():
            btn.pack(side=tk.LEFT, padx=5)

        search_frame = tk.Frame(self, bg="#f4f4f4")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Tìm kiếm:", font=("Arial", 10, "bold"), bg="#f4f4f4").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=30, font=("Arial", 10))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = tk.Button(search_frame, text="Tìm", bg="#ffc107", width=8, font=("Arial", 10, "bold"))
        self.search_button.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=(
        EMPLOYEE_CODE, EMPLOYEE_USERNAME, EMPLOYEE_PASSWORD, EMPLOYEE_ADDRESS, EMPLOYEE_GENDER, EMPLOYEE_BIRTHDATE,
        EMPLOYEE_PHONE, EMPLOYEE_ROLE), show="headings")

        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        style.configure("Treeview.Heading", font=("Tahoma", 10), background="#007bff",
                        foreground="black")  # Đổi chữ thành màu đen

        column_sizes = {
            EMPLOYEE_CODE: 80,
            EMPLOYEE_USERNAME: 120,
            EMPLOYEE_PASSWORD: 100,
            EMPLOYEE_ADDRESS: 150,
            EMPLOYEE_GENDER: 80,
            EMPLOYEE_BIRTHDATE: 100,
            EMPLOYEE_PHONE: 100,
            EMPLOYEE_ROLE: 100
        }

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=column_sizes[col], anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)