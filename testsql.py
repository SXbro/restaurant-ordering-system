#  this file is to check whether the sql is working or not 

import sqlite3

def view_orders():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()

    print("\n=== DINE-IN ORDERS ===")
    c.execute("SELECT * FROM dine_in_orders")
    dine_in = c.fetchall()
    for row in dine_in:
        print(row)

    print("\n=== TAKEOUT ORDERS ===")
    c.execute("SELECT * FROM takeout_orders")
    takeout = c.fetchall()
    for row in takeout:
        print(row)

    conn.close()

if __name__ == "__main__":
    view_orders()
