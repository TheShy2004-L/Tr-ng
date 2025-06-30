import tkinter as tk
from tkinter import ttk


class ProductView(tk.Frame):  # Kế thừa từ tk.Frame
    def __init__(self, parent):
        super().__init__(parent)  # Gọi constructor của tk.Frame
        self.root = parent  # Lưu tham chiếu đến cửa sổ cha
        self.pack(fill="both", expand=True)  # Cho phép tự động mở rộng khi hiển thị

        self.setup_ui()
        self.controller = None  # Khởi tạo controller rỗng
        self.setup_controller()  # Thiết lập controller sau khi UI sẵn sàng

    def setup_ui(self):
        # Tiêu đề
        title_frame = tk.Frame(self, bg="#007bff", padx=10, pady=10)
        title_frame.pack(fill="x")
        title_label = tk.Label(title_frame, text="QUẢN LÝ SẢN PHẨM", fg="white", bg="#007bff",
                               font=("Arial", 16, "bold"))
        title_label.pack()

        # Khung nhập liệu
        form_frame = tk.Frame(self, bg="#f8f9fa", padx=10, pady=10)
        form_frame.pack(fill="x")

        labels = ["Tên SP", "Giá", "Số lượng", "Loại", "Điểm thưởng", "Barcode"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", bg="#f8f9fa", font=("Arial", 12)).grid(row=0, column=i, padx=5)
            if label == "Loại":
                entry = ttk.Combobox(form_frame, values=["Food", "Drink"], state="readonly", width=15)
                entry.current(0)
            else:
                entry = tk.Entry(form_frame, width=18)
            entry.grid(row=1, column=i, padx=5, pady=3)
            self.entries[label] = entry

        # Khung nút chức năng
        button_frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        button_frame.pack(fill="x")

        self.buttons = {
            "Scan to add": tk.Button(button_frame, text="Scan to add", font=("Arial", 12), bg="#28a745", fg="white",
                                     padx=10),
            "Thêm": tk.Button(button_frame, text="Thêm", font=("Arial", 12), bg="#28a745", fg="white", padx=10),
            "Cập nhật": tk.Button(button_frame, text="Cập nhật", font=("Arial", 12), bg="#007bff", fg="white", padx=10),
            "Xóa": tk.Button(button_frame, text="Xóa", font=("Arial", 12), bg="#dc3545", fg="white", padx=10),
            "Làm mới": tk.Button(button_frame, text="Làm mới", font=("Arial", 12), bg="#6c757d", fg="white", padx=10),
        }

        for btn in self.buttons.values():
            btn.pack(side=tk.LEFT, padx=5)

        # Khung tìm kiếm
        search_frame = tk.Frame(self, bg="#f8f9fa", padx=10, pady=10)
        search_frame.pack(fill="x")

        tk.Label(search_frame, text="Tìm kiếm:", bg="#f8f9fa", font=("Arial", 12)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=30, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = tk.Button(search_frame, text="🔍 Tìm", font=("Arial", 12), bg="#ffc107", fg="black",
                                       padx=10)
        self.search_button.pack(side=tk.LEFT)

        # Bảng hiển thị sản phẩm
        table_frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        columns = ["ID", "Mã SP", "Tên SP", "Giá", "Số lượng", "Loại SP", "Điểm thưởng", "Barcode"]
        column_sizes = {"ID": 50, "Mã SP": 80, "Tên SP": 150, "Giá": 100, "Số lượng": 90, "Loại SP": 110,
                        "Điểm thưởng": 80, "Barcode": 80}

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_sizes[col], anchor="center")

        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        style.configure("Treeview.Heading", font=("Tahoma", 10), background="#007bff",
                        foreground="black")  # Đổi chữ thành màu đen

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def setup_controller(self):
        from controllers.product_controller import ProductController  # Import bên trong để tránh vòng lặp
        self.controller = ProductController(self)
        self.controller.load_products()  # Load dữ liệu sau khi controller được thiết lập
