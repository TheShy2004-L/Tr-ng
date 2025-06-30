import tkinter as tk
from calendar import month
from datetime import datetime
from tkinter import ttk, Message, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from pyexpat.errors import messages

from controllers.report_controller import ReportController


class ChartView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True, padx=10, pady=10, ipadx=5, ipady=5)
        self.current_year = datetime.now().year
        self.report_controller = ReportController()
        # Lấy tháng hiện tại để xác định quý
        self.current_month = datetime.now().month
        self.current_quarter = (self.current_month - 1) // 3 + 1
        self.data_in_quarter = self.report_controller.get_data_quarter(self.current_quarter, self.current_year)

        # Tạo dictionary ánh xạ quý với tháng
        self.quarter_months = {
            "Quarter 1 (Jan - Mar)": [1, 2, 3],
            "Quarter 2 (Apr - Jun)": [4, 5, 6],
            "Quarter 3 (Jul - Sep)": [7, 8, 9],
            "Quarter 4 (Oct - Dec)": [10, 11, 12]
        }

        # Chia layout thành 3 phần với màu sắc và viền
        self.top_frame = tk.Frame(self, height=300, bg="#E3F2FD", relief="ridge", bd=2)
        self.bottom_frame = tk.Frame(self, bg="#ECEFF1", relief="ridge", bd=2)

        self.left_frame = tk.Frame(self.bottom_frame, width=400, bg="white", relief="groove", bd=2)
        self.right_frame = tk.Frame(self.bottom_frame, width=400, bg="white", relief="groove", bd=2)

        self.top_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.bottom_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.left_frame.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=2, pady=2)


        # Thêm bộ lọc quý
        self.create_quarter_filter()

        # Vẽ biểu đồ
        self.draw_growth_chart()
        self.draw_stacked_bar_chart()
        self.draw_pie_chart()

    def create_quarter_filter(self):
        """Tạo bộ lọc chọn quý"""
        frame = tk.Frame(self.top_frame, bg="#E3F2FD")
        frame.pack(pady=10)

        tk.Label(frame, text="📅 Select quarter:", font=("Arial", 12, "bold"), bg="#E3F2FD", fg="#1976D2").pack(side="left", padx=5)

        self.quarter_var = tk.StringVar()
        self.quarter_combobox = ttk.Combobox(
            frame, textvariable=self.quarter_var, state="readonly", font=("Arial", 12), width=15
        )
        self.quarter_combobox["values"] = list(self.quarter_months.keys())
        self.quarter_combobox.pack(side="left", padx=5)

        # Chọn quý mặc định
        for key, months in self.quarter_months.items():
            if self.current_month in months:
                self.selected_months = months
                self.selected_quarter = key
                self.current_quarter = (months[1] - 1) // 3 + 1
                self.quarter_combobox.set(key)
                break

        # Nút cập nhật
        self.update_button = tk.Button(frame, text="🔄 Cập nhật", font=("Arial", 12, "bold"),
                                       bg="#1976D2", fg="white", relief="raised", cursor="hand2",
                                       command=self.update_charts)
        self.update_button.pack(side="left", padx=10)

    def update_charts(self):
        """Cập nhật dữ liệu biểu đồ theo quý được chọn"""
        selected_quarter = self.quarter_var.get()
        self.selected_months = self.quarter_months.get(selected_quarter, [])
        self.data_in_quarter = self.report_controller.get_data_quarter(selected_quarter, self.current_year)
        if self.data_in_quarter:
            if not self.selected_months:
                return

            # Xóa biểu đồ cũ
            for widget in self.top_frame.winfo_children():
                widget.destroy()
            for widget in self.left_frame.winfo_children():
                widget.destroy()
            for widget in self.right_frame.winfo_children():
                widget.destroy()

            # Vẽ lại biểu đồ
            self.create_quarter_filter()
            self.draw_growth_chart()
            self.draw_stacked_bar_chart()
            self.draw_pie_chart()
        else:
            messagebox.showinfo(f"Information",f"No data of {selected_quarter}")

    def draw_growth_chart(self):
        month_growth_chart = self.selected_months
        sales = []

        for i in self.data_in_quarter:
            a = i[0]
            sales.append(a[8] / 1000000)  # Chuyển doanh thu sang đơn vị triệu VND

        month_labels = [datetime(1900, m, 1).strftime('%b') for m in month_growth_chart]

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(month_labels, sales, marker='o', linestyle='-', color='#1976D2', label='Doanh thu')

        # Hiển thị số liệu trên từng điểm dữ liệu
        for i, txt in enumerate(sales):
            ax.text(i, sales[i] + 0.1, f"{sales[i]:.1f}", ha='center', fontsize=9, color='#333333', fontweight='bold')

        ax.set_title(f"Revenue chart in {self.selected_quarter}", color="#333333")
        ax.set_xlabel("Month", color="#555555")
        ax.set_ylabel("Revenue (Million VND)", color="#555555")  # Đơn vị triệu đồng
        ax.legend()

        fig.patch.set_facecolor("#E3F2FD")

        canvas = FigureCanvasTkAgg(fig, master=self.top_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        canvas.draw()

    def draw_stacked_bar_chart(self):

            month_labels = [datetime(1900, m, 1).strftime('%b') for m in self.selected_months]

            categories = month_labels
            drink_qty = []
            food_qty = []

            for i in self.data_in_quarter:
                a = i[0]
                drink_qty.append(a[3])  # Số lượng đồ uống
                food_qty.append(a[5])  # Số lượng đồ ăn

            fig, ax = plt.subplots(figsize=(4, 3))
            x = np.arange(len(categories))
            width = 0.6

            # Vẽ cột đồ uống
            bars1 = ax.bar(x, drink_qty, width, label='Quantity of drink', color='#64B5F6')

            # Vẽ cột đồ ăn (chồng lên đồ uống)
            bars2 = ax.bar(x, food_qty, width, bottom=drink_qty, label='Quantity of food', color='#FFB74D')

            # Hiển thị giá trị trên từng cột
            for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
                h1 = bar1.get_height()  # Chiều cao cột đồ uống
                h2 = bar2.get_height()  # Chiều cao cột đồ ăn
                total = h1 + h2  # Tổng số lượng

                # Hiển thị giá trị của đồ uống
                ax.text(bar1.get_x() + bar1.get_width() / 2, h1 / 2, f'{h1}', ha='center', va='center', color='white',
                        fontsize=9)

                # Hiển thị giá trị của đồ ăn
                ax.text(bar2.get_x() + bar2.get_width() / 2, h1 + h2 / 2, f'{h2}', ha='center', va='center',
                        color='white', fontsize=9)

                # Hiển thị tổng giá trị trên đỉnh
                ax.text(bar1.get_x() + bar1.get_width() / 2, total + 5, f'{total}', ha='center', va='bottom',
                        fontsize=10, fontweight='bold', color='#333333')

            ax.set_title(f'Comparison of total product sold in {self.selected_quarter}', color="#333333")
            ax.set_xlabel('Month', color="#555555")
            ax.set_ylabel('Quantity', color="#555555")
            ax.set_xticks(x)
            ax.set_xticklabels(categories)
            ax.legend()

            fig.patch.set_facecolor("#FFFFFF")

            canvas = FigureCanvasTkAgg(fig, master=self.left_frame)
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            canvas.draw()

    def draw_pie_chart(self):
        total_price_drink = 0
        total_price_food = 0

        for i in self.data_in_quarter:
            data = i[0]
            total_price_drink += data[4]
            total_price_food += data[6]

        total = total_price_drink + total_price_food
        labels = ["Food Total Price", "Drink Total Price"]
        sizes = [(total_price_food / total * 100), 100 - (total_price_food / total * 100)]
        colors = ['#64B5F6', '#FFB74D']

        fig, ax = plt.subplots(figsize=(4, 3))

        # Hiển thị giá trị cụ thể trong biểu đồ tròn
        def func(pct, all_values):
            absolute = int(round(pct / 100. * sum(all_values)))
            return f"{pct:.1f}%\n({absolute:,} VND)"  # Hiển thị phần trăm & số tiền

        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct=lambda pct: func(pct, [total_price_food, total_price_drink]),
            colors=colors, startangle=90, textprops={'fontsize': 9, 'color': "#333333"}
        )

        ax.set_title(f"Comparison of Food & Drink Revenue in {self.selected_quarter}", color="#333333")

        fig.patch.set_facecolor("#FFFFFF")

        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        canvas.draw()


