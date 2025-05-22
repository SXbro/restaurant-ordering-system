# 🍽️ Smart Restaurant Ordering System (Python GUI + SQLite)

Welcome to the **Smart Restaurant Ordering System**, a Python GUI application designed for small to medium-sized restaurants to simplify order management, track sales, and save costs on paper or tablet menus. With both dine-in and takeout options, the system stores data efficiently in a local SQLite database and provides a user-friendly interface.

---

## 🔍 What Is This Project?

This is more than a code project—it's a **solution** to a real-world problem. It allows restaurant owners to:

- Collect orders from customers (food, drink, dessert)
- Choose between **Dine-in** or **Takeout**
- Automatically **calculate total cost**
- Store all data into a **SQLite database**
- Visualize and process orders without expensive tech

---

## 🛠 Features

✅ Dine-in and Takeout mode  
✅ Food, Drinks, Desserts selection  
✅ Total cost calculation  
✅ Delivery info form for takeout  
✅ Real-time progress bar for dine-in  
✅ SQLite database integration  
✅ Data saving and display in terminal  
✅ Simple, intuitive GUI using Tkinter

---

## 🧰 Technologies Used

- 🐍 Python 3
- 🖼️ Tkinter (for GUI)
- 💾 SQLite (for local data storage)
- 🧠 Custom functions and classes

---

How It Works

For Dine-in Customers:
User selects food, drink, and dessert
Clicks “Order”
Order is saved into orders.db
A progress bar simulates order processing
A “Thank You” message is shown
For Takeout Customers:
After selecting items, a delivery form pops up
User enters name, phone number, and address
Data is saved into the database
Order info is printed in the terminal

Future Improvements

Export order history to Excel/CSV
Admin dashboard for analytics
QR Code menu access from tables
Cloud sync options


## 📦 Installation

```bash
git clone https://github.com/SXbro/restaurant-ordering-system.git
cd restaurant-ordering-system
python main.py
