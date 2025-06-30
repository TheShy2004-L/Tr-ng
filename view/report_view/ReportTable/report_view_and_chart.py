import tkinter as tk
from tkinter import ttk

from view.report_view.ReportTable.report_view import ReportView
from view.report_view.ReportView.chart_view import ChartView


class ReportViewAndChart(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)  # Cho phép mở rộng khi hiển thị

        # Tạo Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Tạo Frame cho từng tab
        self.tab1 = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.tab2 = ttk.Frame(self.notebook, style="Custom.TFrame")

        self.notebook.add(self.tab1, text="📊 Report Chart")
        self.notebook.add(self.tab2, text="📋 Report Table")

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        self.tab1_loaded = False
        self.tab2_loaded = False

        # Áp dụng style hiện đại
        self.apply_styles()

    def apply_styles(self):
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f8f9fa")
        style.configure("TNotebook", background="#E6E6FA")
        style.configure("TNotebook.Tab", background="#87CEFA", font=("Arial", 12, "bold"), padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#007bff")])

    def on_tab_selected(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 0 and not self.tab1_loaded:
            ChartView(self.tab1)
            self.tab1_loaded = True

        if selected_tab == 1 and not self.tab2_loaded:
            ReportView(self.tab2)
            self.tab2_loaded = True


