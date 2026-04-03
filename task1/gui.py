import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from product import FreshFood, Groceries, Household, Product
from inventory import Inventory

class system_GUI:
    # Encapsulation: include all user interface components
    def __init__(self, root):
        self.root = root
        self.root.title("Supermarket Inventory System")
        self.root.geometry("1250x550")

        self.inventory = Inventory()
        self._setup_ui()
        self._add_sample_data()
        self._auto_update_table()

    # Inheritance: created some objects
    def _add_sample_data(self):
        self.inventory.add_product(FreshFood("Del Monte", "Banana 5 pcs", 5, 50, "pack"))
        self.inventory.add_product(Groceries("Coca Cola", "Coke 8 pcs", 20, 100, "pack"))
        self.inventory.add_product(Household("Vinda", "Tissue 12 rolls", 15, 300, "pack"))

    def _setup_ui(self):
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 15), pady=5)

        columns = ("product_no", "type", "supplier", "description", "cost", "selling_price", "quantity", "unit", "last_action", "last_action_date")
        self.table = ttk.Treeview(left_frame, columns=columns, show="headings")

        self.table.heading("product_no", text="Product No")
        self.table.heading("type", text="Type")
        self.table.heading("supplier", text="Supplier")
        self.table.heading("description", text="Description")
        self.table.heading("cost", text="Cost")
        self.table.heading("selling_price", text="Selling Price")
        self.table.heading("quantity", text="Quantity")
        self.table.heading("unit", text="Unit")
        self.table.heading("last_action", text="Last Action")
        self.table.heading("last_action_date", text="Last Action Date")

        self.table.column("product_no", width=80)
        self.table.column("type", width=100)
        self.table.column("supplier", width=100)
        self.table.column("description", width=150)
        self.table.column("cost", width=60)
        self.table.column("selling_price", width=80)
        self.table.column("quantity", width=60)
        self.table.column("unit", width=60)
        self.table.column("last_action", width=100)
        self.table.column("last_action_date", width=140)

        self.table.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.status_label = ttk.Label(left_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 5), pady=5)

        ttk.Button(right_frame, text="Add", command=self.add_product).pack(fill=tk.X, pady=2)
        ttk.Button(right_frame, text="Restock", command=self.restock_product).pack(fill=tk.X, pady=2)
        ttk.Button(right_frame, text="Sell", command=self.sell_product).pack(fill=tk.X, pady=2)
        ttk.Button(right_frame, text="Delete", command=self.delete_product).pack(fill=tk.X, pady=2)
        ttk.Button(right_frame, text="Records", command=self.show_record).pack(fill=tk.X, pady=2)

    # Private method: refresh product list in the table
    def _auto_update_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        # Sorting use __lt__ magic method from Product class
        all_products = sorted(self.inventory.get_products())
        for product in all_products:
            latest = self.inventory.get_last_record(product.get_description())
            if latest:
                # Last Action shows operation and quantity with "qty" suffix
                last_action = f"{latest.get_operation()} {latest.get_quantity()} qty"
                last_action_date = latest.get_timestamp()
            else:
                last_action = ""
                last_action_date = ""

            # Polymorphism: get_selling_price()
            if isinstance(product, FreshFood):
                type_display = "Fresh Food"
            elif isinstance(product, Groceries):
                type_display = "Groceries"
            elif isinstance(product, Household):
                type_display = "Household"
            else:
                type_display = ""

            self.table.insert("", tk.END, values=(
                product.get_product_no(),
                type_display,
                product.get_supplier(),
                product.get_description(),
                f"${product.get_cost():.2f}",
                f"${product.get_selling_price():.2f}",
                product.get_quantity(),
                product.get_unit(),
                last_action,
                last_action_date
            ))

        current_count = len(all_products)
        # Class method: Call the class itself
        total_ever = Product.get_total_products()
        self.status_label.config(text=f"Total number of product: {current_count} | Total number of product added: {total_ever}")

    # Private helper: returns selected row
    def _get_selected_row(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product from the list")
            return None
        return self.table.item(selected[0])

    # Public methods
    def add_product(self):
        window = tk.Toplevel(self.root)
        window.title("Add Product")
        window.geometry("350x350")

        ttk.Label(window, text="Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        type_var = tk.StringVar(value="Fresh Food")
        ttk.Combobox(window, textvariable=type_var, values=["FreshFood", "Groceries", "Household"]).grid(row=0, column=1)

        ttk.Label(window, text="Supplier:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        supplier_entry = ttk.Entry(window)
        supplier_entry.grid(row=1, column=1)

        ttk.Label(window, text="Description:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        description_entry = ttk.Entry(window)
        description_entry.grid(row=2, column=1)

        ttk.Label(window, text="Cost:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        cost_entry = ttk.Entry(window)
        cost_entry.grid(row=3, column=1)

        ttk.Label(window, text="Unit:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        unit_entry = ttk.Entry(window)
        unit_entry.grid(row=4, column=1)

        ttk.Label(window, text="Quantity:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        quantity_entry = ttk.Entry(window)
        quantity_entry.grid(row=5, column=1)

        # Input validation
        def validate_input():
            try:
                supplier = supplier_entry.get().strip()
                description = description_entry.get().strip()
                cost_text = cost_entry.get().strip()
                unit = unit_entry.get().strip()
                quantity_text = quantity_entry.get().strip()

                if not supplier:
                    raise ValueError("Supplier is required")
                if not description:
                    raise ValueError("Description is required")
                if not unit:
                    raise ValueError("Unit is required")
                if not cost_text:
                    raise ValueError("Cost is required")
                try:
                    cost = int(cost_text)
                except ValueError:
                    raise ValueError("Cost must be a valid integer")

                if not Product.is_valid_cost(cost):
                    raise ValueError("Cost must be a valid integer")

                quantity = 0
                if quantity_text:
                    try:
                        quantity = int(quantity_text)
                    except ValueError:
                        raise ValueError("Quantity must be a valid integer")
                if quantity < 0:
                    raise ValueError("Quantity must be a valid integer")

                if type_var.get() == "FreshFood":
                    product = FreshFood(supplier, description, cost, quantity, unit)
                elif type_var.get() == "Groceries":
                    product = Groceries(supplier, description, cost, quantity, unit)
                else:
                    product = Household(supplier, description, cost, quantity, unit)

                self.inventory.add_product(product)
                self._auto_update_table()
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(window, text="OK", command=validate_input).grid(row=6, column=0, pady=10)
        ttk.Button(window, text="Cancel", command=window.destroy).grid(row=6, column=1)

    def restock_product(self):
        item = self._get_selected_row()
        if item is None:
            return
        description = item['values'][3]

        qty = simpledialog.askinteger("Restock", f"Enter quantity to add for {description}:", minvalue=1)
        if qty is None:
            return
        product = self.inventory.find_product(description)
        if product is None:
            messagebox.showerror("Error", f"Product '{description}' not found.")
            return
        if self.inventory.restock_product(description, qty):
            self._auto_update_table()
            messagebox.showinfo("Success", f"{description} added {qty} quantity")

    def sell_product(self):
        item = self._get_selected_row()
        if item is None:
            return
        description = item['values'][3]

        while True:
            qty = simpledialog.askinteger("Sell", f"Enter quantity to sell for {description}:", minvalue=1)
            if qty is None:
                return
            product = self.inventory.find_product(description)
            if product is None:
                messagebox.showerror("Error", f"Product '{description}' not found.")
                return
            if product.get_quantity() < qty:
                messagebox.showerror("Error", f"Product '{description}' has insufficient stock. Existing quantity: {product.get_quantity()}")
                continue
            if self.inventory.sell_product(description, qty):
                self._auto_update_table()
                messagebox.showinfo("Success", f"{description} sold {qty} quantity")
                return
            messagebox.showerror("Error", f"Sell failed for '{description}'.")
            return

    def delete_product(self):
        item = self._get_selected_row()
        if item is None:
            return
        description = item['values'][3]

        if messagebox.askyesno("Confirm", f"Delete {description}?"):
            product = self.inventory.find_product(description)
            if product is None:
                messagebox.showerror("Error", f"Product '{description}' not found.")
                return
            if self.inventory.delete_product(description):
                self._auto_update_table()
                messagebox.showinfo("Success", "Product deleted")

    def show_record(self):
        item = self._get_selected_row()
        if item is None:
            return
        description = item['values'][3]

        all_records = self.inventory.get_records()
        product_records = [r for r in all_records if r.get_description() == description]

        if not product_records:
            messagebox.showinfo("Record", f"No records for {description}.")
            return

        record_win = tk.Toplevel(self.root)
        record_win.title(f"Records - {description}")
        record_win.geometry("600x400")

        text_area = tk.Text(record_win, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(record_win, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for record in reversed(product_records):
            text_area.insert(tk.END, str(record) + "\n\n")
        text_area.config(state=tk.DISABLED)
