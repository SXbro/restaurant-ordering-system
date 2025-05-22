import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import time
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS dine_in_orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    food TEXT,
                    drink TEXT,
                    dessert TEXT,
                    total_cost REAL,
                    timestamp TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS takeout_orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    food TEXT,
                    drink TEXT,
                    dessert TEXT,
                    total_cost REAL,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# GUI setup
class MealOrderingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meal Ordering System")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f8ff")  # light blue

        self.food_items = {"Pizza": 8, "Burger": 6, "Pasta": 7, "Salad": 5}
        self.drinks = {"Water": 1, "Coke": 2, "Juice": 3}
        self.desserts = {"Ice Cream": 3, "Cake": 4, "Fruit Salad": 3}

        self.selected_food = {}
        self.selected_drink = tk.StringVar()
        self.selected_dessert = tk.StringVar()
        self.total_cost = tk.DoubleVar()

        self.order_type = None  # 'dine_in' or 'takeout'

        self.create_start_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_start_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to Our Meal Service", font=("Arial", 20), bg="#f0f8ff", fg="black").pack(pady=20)
        tk.Button(self.root, text="Dine-In Order", command=self.start_dine_in_order, width=20, height=2, bg="#4682b4", fg="black").pack(pady=10)
        tk.Button(self.root, text="Takeout Order", command=self.start_takeout_order, width=20, height=2, bg="#5f9ea0", fg="black").pack(pady=10)

    def start_dine_in_order(self):
        self.order_type = 'dine_in'
        self.create_menu_screen()

    def start_takeout_order(self):
        self.order_type = 'takeout'
        self.create_menu_screen()

    def create_menu_screen(self):
        self.clear_screen()
        self.selected_food = {}
        self.selected_drink.set("")
        self.selected_dessert.set("")
        self.total_cost.set(0)

        tk.Label(self.root, text="Choose Your Meal", font=("Arial", 16), bg="#f0f8ff", fg="black").pack(pady=10)

        frame = tk.Frame(self.root, bg="#f0f8ff")
        frame.pack(pady=10)

        # Food
        food_frame = tk.LabelFrame(frame, text="Food", bg="#f0f8ff", fg="black")
        food_frame.grid(row=0, column=0, padx=10)
        for food, price in self.food_items.items():
            var = tk.BooleanVar()
            cb = tk.Checkbutton(food_frame, text=f"{food} (${price})", variable=var, bg="#f0f8ff", fg="black")
            cb.pack(anchor='w')
            self.selected_food[food] = var

        # Drink
        drink_frame = tk.LabelFrame(frame, text="Drink", bg="#f0f8ff", fg="black")
        drink_frame.grid(row=0, column=1, padx=10)
        for drink, price in self.drinks.items():
            rb = tk.Radiobutton(drink_frame, text=f"{drink} (${price})", variable=self.selected_drink, value=drink, bg="#f0f8ff", fg="black")
            rb.pack(anchor='w')

        # Dessert
        dessert_frame = tk.LabelFrame(frame, text="Dessert", bg="#f0f8ff", fg="black")
        dessert_frame.grid(row=0, column=2, padx=10)
        for dessert, price in self.desserts.items():
            rb = tk.Radiobutton(dessert_frame, text=f"{dessert} (${price})", variable=self.selected_dessert, value=dessert, bg="#f0f8ff", fg="black")
            rb.pack(anchor='w')

        # Total cost
        tk.Label(self.root, textvariable=self.total_cost, font=("Arial", 14), bg="#f0f8ff", fg="black").pack(pady=10)
        self.update_cost()
        self.root.after(1000, self.update_cost)

        tk.Button(self.root, text="Next", command=self.next_screen, bg="#20b2aa", fg="black").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_start_screen, fg="black").pack()

    def update_cost(self):
        total = 0
        for food, var in self.selected_food.items():
            if var.get():
                total += self.food_items[food]
        if self.selected_drink.get():
            total += self.drinks[self.selected_drink.get()]
        if self.selected_dessert.get():
            total += self.desserts[self.selected_dessert.get()]
        self.total_cost.set(total)
        self.root.after(1000, self.update_cost)

    def next_screen(self):
        if self.order_type == 'dine_in':
            self.confirm_dine_in_order()
        elif self.order_type == 'takeout':
            self.collect_takeout_info()

    def confirm_dine_in_order(self):
        self.clear_screen()
        tk.Label(self.root, text="Confirming Your Dine-In Order", font=("Arial", 16), bg="#f0f8ff", fg="black").pack(pady=20)
        tk.Button(self.root, text="Confirm", command=self.process_dine_in_order, bg="#32cd32", fg="black").pack(pady=10)

    def process_dine_in_order(self):
        foods = [food for food, var in self.selected_food.items() if var.get()]
        drink = self.selected_drink.get()
        dessert = self.selected_dessert.get()
        total = self.total_cost.get()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("DINE-IN ORDER")
        print("Food:", foods)
        print("Drink:", drink)
        print("Dessert:", dessert)
        print("Total:", total)

        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute("INSERT INTO dine_in_orders (food, drink, dessert, total_cost, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (", ".join(foods), drink, dessert, total, timestamp))
        conn.commit()
        conn.close()

        self.show_progress_bar()

    def collect_takeout_info(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter Delivery Information", font=("Arial", 16), bg="#f0f8ff", fg="black").pack(pady=10)

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_text = tk.Text(self.root, height=3, width=40)

        tk.Label(self.root, text="Full Name:", bg="#f0f8ff", fg="black").pack()
        tk.Entry(self.root, textvariable=self.name_var).pack()
        tk.Label(self.root, text="Phone Number:", bg="#f0f8ff", fg="black").pack()
        tk.Entry(self.root, textvariable=self.phone_var).pack()
        tk.Label(self.root, text="Email (optional):", bg="#f0f8ff", fg="black").pack()
        tk.Entry(self.root, textvariable=self.email_var).pack()
        tk.Label(self.root, text="Address:", bg="#f0f8ff", fg="black").pack()
        self.address_text.pack()

        tk.Button(self.root, text="Submit Order", command=self.process_takeout_order, bg="#ff8c00", fg="black").pack(pady=10)

    def process_takeout_order(self):
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        address = self.address_text.get("1.0", tk.END).strip()

        if not name or not phone or not address:
            messagebox.showerror("Input Error", "Please fill in all required fields.")
            return

        foods = [food for food, var in self.selected_food.items() if var.get()]
        drink = self.selected_drink.get()
        dessert = self.selected_dessert.get()
        total = self.total_cost.get()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("TAKEOUT ORDER")
        print("Name:", name)
        print("Phone:", phone)
        print("Email:", email)
        print("Address:", address)
        print("Food:", foods)
        print("Drink:", drink)
        print("Dessert:", dessert)
        print("Total:", total)

        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute("INSERT INTO takeout_orders (name, phone, email, address, food, drink, dessert, total_cost, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, phone, email, address, ", ".join(foods), drink, dessert, total, timestamp))
        conn.commit()
        conn.close()

        messagebox.showinfo("Order Received", "Thank you for your order!")
        self.create_start_screen()

    def show_progress_bar(self):
        self.clear_screen()
        tk.Label(self.root, text="Preparing your order...", font=("Arial", 16), bg="#f0f8ff", fg="black").pack(pady=20)
        pb = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        pb.pack(pady=20)

        def fill():
            for i in range(0, 101, 10):
                pb["value"] = i
                self.root.update_idletasks()
                time.sleep(0.5)
            tk.Label(self.root, text="Thanks for using our service! Your meal will be served shortly.", bg="#f0f8ff", fg="green").pack(pady=10)
            tk.Button(self.root, text="Back to Start", command=self.create_start_screen, fg="black").pack(pady=10)

        self.root.after(100, fill)

if __name__ == "__main__":
    root = tk.Tk()
    app = MealOrderingApp(root)
    root.mainloop()