import tkinter as tk

from view.main_view.home import MainApp
from view.main_view.login_view import LoginView


def run():
    root = tk.Tk()  # Tạo cửa sổ Tkinter
    with open(r"D:\BTL_Python_done1603\resource\user.txt", "r") as file:
        data = file.read().strip()  # Đọc toàn bộ nội dung và loại bỏ khoảng trắng
    if data == "None":
        app = LoginView(root)  # Truyền root vào AdminDashboard
        root.mainloop()  # Chạy vòng lặp Tkinter
    else:
        MainApp(root)
        root.mainloop()


if __name__ == "__main__":
    run()




