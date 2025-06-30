import tkinter as tk
from tkinter import ttk, messagebox
from controllers.customer_controller import CustomerController


class CustomerView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = CustomerController()
        self.pack(fill="both", expand=True)
        self.configure(bg="#f8f9fa")  # Light background color
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self, bg="#007bff", padx=10, pady=10)
        title_frame.pack(fill="x")
        title_label = tk.Label(title_frame, text="CUSTOMER MANAGEMENT", fg="white", bg="#007bff",
                               font=("Arial", 16, "bold"))
        title_label.pack()

        # Input area
        input_frame = ttk.LabelFrame(self, text="Customer Information", padding="10")
        input_frame.pack(fill="x", padx=10, pady=10)

        labels = ["Customer Name", "Phone Number", "Address"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(input_frame, text=label + ":", font=("Arial", 10)).grid(row=i, column=0, padx=5, pady=5,
                                                                             sticky="e")
            entry = ttk.Entry(input_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries[label] = entry

        # Button area
        button_frame = tk.Frame(self, bg="#f8f9fa")
        button_frame.pack(fill="x", padx=10, pady=5)

        self.add_button = ttk.Button(button_frame, text="Add", command=self.add_customer)
        self.edit_button = ttk.Button(button_frame, text="Edit", command=self.show_customer_list)
        self.save_button = ttk.Button(button_frame, text="Save", command=self.update_customer, state="disabled")
        self.delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_customer)

        for btn in [self.add_button, self.edit_button, self.save_button, self.delete_button]:
            btn.pack(side=tk.LEFT, padx=5, pady=5, expand=True)

        # Search area
        search_frame = ttk.LabelFrame(self, text="Search", padding="10")
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Enter keyword:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = ttk.Button(search_frame, text="Search", command=self.search_customer)
        self.search_button.pack(side=tk.LEFT, padx=5)

        # Customer data display table
        tree_frame = tk.Frame(self, bg="#f8f9fa")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        style.configure("Treeview.Heading", font=("Tahoma", 10), background="#007bff",
                        foreground="black")  # Change text color to black
        columns = ("ID", "Name", "Phone", "Address", "Loyalty Points", "Created Date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.load_customers()
        self.selected_id = None

    def load_customers(self):
        self.tree.delete(*self.tree.get_children())
        success, result = self.controller.get_all_customers()
        if success:
            for row in sorted(result, key=lambda x: x[0]):
                self.tree.insert("", 'end', values=row)
        else:
            messagebox.showerror("Error", result)

    def add_customer(self):
        success, message = self.controller.add_customer(self.entries["Customer Name"].get(),
                                                        self.entries["Phone Number"].get(),
                                                        self.entries["Address"].get())
        if success:
            messagebox.showinfo("Notification", message)
            self.load_customers()
        else:
            messagebox.showerror("Error", message)

    def show_customer_list(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a customer to edit!")
            return
        row_data = self.tree.item(selected_item[0], "values")
        self.selected_id = row_data[0]
        self.entries["Customer Name"].delete(0, tk.END)
        self.entries["Customer Name"].insert(0, row_data[1])
        self.entries["Phone Number"].delete(0, tk.END)
        self.entries["Phone Number"].insert(0, row_data[2])
        self.entries["Address"].delete(0, tk.END)
        self.entries["Address"].insert(0, row_data[3])
        self.save_button["state"] = "normal"

    def update_customer(self):
        if self.selected_id is None:
            messagebox.showerror("Error", "Please select a customer from the list first!")
            return
        success, message = self.controller.update_customer(self.selected_id, self.entries["Customer Name"].get(),
                                                           self.entries["Phone Number"].get(),
                                                           self.entries["Address"].get())
        if success:
            messagebox.showinfo("Notification", message)
            self.load_customers()
            self.selected_id = None
            self.save_button["state"] = "disabled"
        else:
            messagebox.showerror("Error", message)

    def delete_customer(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a customer to delete!")
            return
        customer = self.tree.item(selected_item)['values']
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete this customer?"):
            success, message = self.controller.delete_customer(customer[0])
            if success:
                messagebox.showinfo("Notification", message)
                self.load_customers()
            else:
                messagebox.showerror("Error", message)

    def search_customer(self):
        self.tree.delete(*self.tree.get_children())
        success, result = self.controller.search_customer(self.search_entry.get())
        if success:
            for row in sorted(result, key=lambda x: x[0]):
                self.tree.insert("", 'end', values=row)
        else:
            messagebox.showerror("Error", result)
