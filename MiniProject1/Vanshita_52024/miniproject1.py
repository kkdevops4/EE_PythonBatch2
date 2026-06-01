#declaring an dictionary
inventory = {}

#declaring an empty list
sales_history = []

#functing for adding product
def add_product():
    pid = int(input("Enter Product ID: "))

    #if product is already exists then show below message
    if pid in inventory:
        print("Product already exists.")
        return

    name = input("Enter Product Name: ")
    price = float(input("Enter Price: "))
    qty = int(input("Enter Quantity: "))

    inventory[pid] = {
        "name": name,
        "price": price,
        "qty": qty
    }

    print("Product Added Successfully")

#function for checking products
def view_products():

    if not inventory:
        print("No products available")
        return

    print("\nId\tName\tPrice\tQuantity")

    for pid, details in inventory.items():
        print(pid,
              details["name"],
              details["price"],
              details["qty"],
              sep="\t")


def sell_product():

    pid = int(input("Enter Product ID: "))

    if pid not in inventory:
        print("Product not found")
        return

    qty = int(input("Enter Quantity Sold: "))

    if qty > inventory[pid]["qty"]:
        print("Insufficient Stock")
        return

    inventory[pid]["qty"] -= qty

    amount = qty * inventory[pid]["price"]

    sales_history.append((pid, qty, amount))

    print("Sale Successful")
    print("Bill Amount =", amount)


def restock_product():

    pid = int(input("Enter Product ID: "))

    if pid not in inventory:
        print("Product not found")
        return

    qty = int(input("Enter Quantity to Add: "))

    inventory[pid]["qty"] += qty

    print("Stock Updated")


def low_stock():

    print("\nLow Stock Products")

    found = False

    for pid, details in inventory.items():

        if details["qty"] < 5:
            print(pid, details["name"], details["qty"])
            found = True

    if not found:
        print("No low stock products")


def inventory_value():

    total = 0

    for details in inventory.values():
        total += details["price"] * details["qty"]

    print("Total Inventory Value =", total)


def search_product():

    name = input("Enter Product Name: ").lower()

    found = False

    for pid, details in inventory.items():

        if name in details["name"].lower():
            print(pid,
                  details["name"],
                  details["price"],
                  details["qty"])
            found = True

    if not found:
        print("Product not found")


while True:

    print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
    print("1. Add Product")
    print("2. View Products")
    print("3. Sell Product")
    print("4. Restock Product")
    print("5. Low Stock Alert")
    print("6. Total Inventory Value")
    print("7. Search Product")
    print("8. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_product()

    elif choice == "2":
        view_products()

    elif choice == "3":
        sell_product()

    elif choice == "4":
        restock_product()

    elif choice == "5":
        low_stock()

    elif choice == "6":
        inventory_value()

    elif choice == "7":
        search_product()

    elif choice == "8":
        print("Thank You")
        break

    else:
        print("Invalid Choice")