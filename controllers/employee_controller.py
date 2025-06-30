import tkinter as tk
from tkinter import messagebox

from config1.config import *

from models.employe_model import EmployeeModel


class EmployeeController:
    def __init__(self, view):
        self.view = view
        self.model = EmployeeModel()
        self.view.buttons["Thêm"].config(command=self.add_employee)
        self.view.buttons["Sửa"].config(command=self.update_employee)
        self.view.buttons["Xóa"].config(command=self.delete_employee)
        self.view.buttons["Làm mới"].config(command=self.load_employees)
        self.view.search_button.config(command=self.search_employee)

        self.load_employees()
        self.view.tree.bind("<ButtonRelease-1>", self.select_employee)

    def load_employees(self):
        rows = self.model.get_all_employees()
        self.view.tree.delete(*self.view.tree.get_children())
        for row in rows:
            self.view.tree.insert("", tk.END, values=row[1:])

    def add_employee(self):
        data = {key: entry.get() for key, entry in self.view.entries.items()}

        # Kiểm tra dữ liệu đầu vào
        if not all(data.values()):
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        success, message = self.model.add_employee(
            data[EMPLOYEE_USERNAME], data[EMPLOYEE_PASSWORD],
            data[EMPLOYEE_ADDRESS], data[EMPLOYEE_GENDER], data[EMPLOYEE_BIRTHDATE],
            data[EMPLOYEE_PHONE], data[EMPLOYEE_ROLE]
        )

        if success:
            self.load_employees()
            messagebox.showinfo("Thành công", message)
        else:
            messagebox.showerror("Lỗi", message)

    def update_employee(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn nhân viên để cập nhật!")
            return

        item_values = self.view.tree.item(selected_item[0], "values")
        emp_id = item_values[0]

        data = {key: entry.get() for key, entry in self.view.entries.items()}

        if not all(data.values()):
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        self.model.update_employee(emp_id,data[EMPLOYEE_USERNAME], data[EMPLOYEE_PASSWORD],
                                   data[EMPLOYEE_ADDRESS], data[EMPLOYEE_GENDER],
                                   data[EMPLOYEE_BIRTHDATE],
                                   data[EMPLOYEE_PHONE],
                                   data[EMPLOYEE_ROLE])
        self.load_employees()
        messagebox.showinfo("Thành công", "Cập nhật nhân viên thành công!")

    def delete_employee(self):
        selected_item = self.view.tree.selection()
        if selected_item:
            item_values = self.view.tree.item(selected_item[0], "values")
            emp_id = item_values[0]
            self.model.delete_employee(emp_id)
            self.load_employees()
            messagebox.showinfo("Thành công", "Xóa nhân viên thành công!")

    def search_employee(self):
        keyword = self.view.search_entry.get()
        rows = self.model.search_employee(keyword)
        self.view.tree.delete(*self.view.tree.get_children())
        for row in rows:
            self.view.tree.insert("", tk.END, values=row[1:])

    def select_employee(self, event):
        selected_item = self.view.tree.selection()
        if not selected_item:
            return

        item_values = self.view.tree.item(selected_item[0], "values")

        # Đổ dữ liệu vào các ô nhập liệu
        self.view.entries[EMPLOYEE_CODE].delete(0, tk.END)
        self.view.entries[EMPLOYEE_CODE].insert(0, item_values[0])  # Username

        self.view.entries[EMPLOYEE_USERNAME].delete(0, tk.END)
        self.view.entries[EMPLOYEE_USERNAME].insert(0, item_values[1])  # Không hiển thị mật khẩu

        self.view.entries[EMPLOYEE_PASSWORD].delete(0, tk.END)
        self.view.entries[EMPLOYEE_PASSWORD].insert(0, item_values[2])  # Employee Code

        self.view.entries[EMPLOYEE_ADDRESS].delete(0, tk.END)
        self.view.entries[EMPLOYEE_ADDRESS].insert(0, item_values[3])  # Address

        self.view.entries[EMPLOYEE_GENDER].set(item_values[4])  # Gender (Combobox)

        self.view.entries[EMPLOYEE_BIRTHDATE].delete(0, tk.END)
        self.view.entries[EMPLOYEE_BIRTHDATE].insert(0, item_values[5])  # Birthdate

        self.view.entries[EMPLOYEE_PHONE].delete(0, tk.END)
        self.view.entries[EMPLOYEE_PHONE].insert(0, item_values[6])  # Phone

        self.view.entries[EMPLOYEE_ROLE].delete(0, tk.END)
        self.view.entries[EMPLOYEE_ROLE].insert(0, item_values[7])  # Role
