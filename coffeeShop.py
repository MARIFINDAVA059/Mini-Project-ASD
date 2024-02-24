from prettytable import PrettyTable
from datetime import datetime

class CoffeeShop:
   def __init__(self):
      self.items = {
            "Espresso": {"price": 5000, "stock": 100},
            "Latte": {"price": 7000, "stock": 100},
            "Cappuccino": {"price": 6000, "stock": 100},
            "Mocha": {"price": 6500, "stock": 100},
            "Macchiato": {"price": 5500, "stock": 100}
      }
      self.users = {}
      self.orders = {}
      self.logged_in_user = None
      self.nama_customer = None
      self.total_income = 0 

   def display_menu_and_stock(self):
      table = PrettyTable(["Menu", "Price", "Stock"])
      for item, info in self.items.items():
            table.add_row([item, info["price"], info["stock"]])
      print("Coffee Shop Menu and Stock")
      print(table)

   def update_menu_and_stock(self):
      self.display_menu_and_stock()
      item = input("Enter the item to update: ")
      if item in self.items:
            price = int(input("Enter the new price: "))
            quantity = int(input("Enter the new stock quantity: "))
            self.items[item]["price"] = price
            self.items[item]["stock"] = quantity
            print(f"Menu item '{item}' updated successfully.")
      else:
            print(f"Menu item '{item}' not found.")

   def delete_menu(self):
      self.display_menu_and_stock()
      item = input("Enter the item to delete: ")
      if item in self.items:
            del self.items[item]
            print(f"Menu item '{item}' deleted successfully.")
      else:
            print(f"Menu item '{item}' not found.")

   def place_order(self, customer_name, coffee_name, quantity):
      if customer_name in self.orders:
         if coffee_name in self.orders[customer_name]:
            self.orders[customer_name][coffee_name] += quantity
         else:
            self.orders[customer_name][coffee_name] = quantity
      else:
         self.orders[customer_name] = {coffee_name: quantity}


   def register_user(self, username, password):
      if username not in self.users:
            self.users[username] = {"password": password, "role": "customer", "balance": 0}
            print("Registration successful.")
      else:
            print("Username already exists. Please choose another username.")

   def login(self, username, password):
      if username in self.users and self.users[username]["password"] == password:
            self.logged_in_user = username
            return True
      return False

   def save_invoice_to_txt(self, customer_name, customer_order, total_bill):
      with open(f'{customer_name}_invoice.txt', 'w') as invoice_file:
            invoice_file.write("CoffeeShop Invoice\n")
            invoice_file.write(f"Customer Name: {customer_name}\n")
            for coffee, quantity in customer_order.items():
               invoice_file.write(f"{coffee}: {quantity}\n")
            invoice_file.write(f"Total Bill: Rp. {total_bill:.2f}\n")

   def generate_invoice(self, customer_name, customer_order, total_bill):
      invoice = PrettyTable()
      invoice.field_names = ["CoffeeShop", "Invoice"]
      invoice.add_row(["Customer Name:", customer_name])
      invoice.add_row(["Transaction Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
      for coffee, quantity in customer_order.items():
            invoice.add_row([coffee, f"{quantity}"])
      invoice.add_row(["Total Bill:", f"Rp. {total_bill:.2f}"])
      print(invoice)
      self.save_invoice_to_txt(customer_name, customer_order, total_bill)

   def register(self):
      print("Welcome To Coffee Shop \nPlease Register First❤️")
      username = input("Enter your username: ")
      password = input("Enter your password: ")
      self.register_user(username, password)

   def login_screen(self):
      while True:
            print("Login Your Account✌️")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if self.login(username, password):
               print(f"Welcome, {username}!")
               break
            else:
               print("Invalid username or password. Please try again.")

   def display_main_menu(self):
      main_menu = PrettyTable()
      main_menu.field_names = ["Features", "CoffeeShop Hanei"]
      main_menu.add_row(["1", "Display Menu & Stock"])
      main_menu.add_row(["2", "Update Menu & Stock"])
      main_menu.add_row(["3", "Delete Menu"])
      main_menu.add_row(["4", "Input Orders"])
      main_menu.add_row(["5", "View Orders"])
      main_menu.add_row(["6", "Total Income"])  
      main_menu.add_row(["7", "Exit"])
      print(main_menu)

   def display_total_income(self):
      print(f"Total Income: Rp. {self.total_income}")

   def display_orders(self):
      orders_table = PrettyTable(["Customer Name", "Order"])
      for customer, order in self.orders.items():
         if isinstance(order, int):
            coffee_name = None
            for coffee, info in self.items.items():
               if info["price"] == order:
                  coffee_name = coffee
                  break
            if coffee_name:
               orders_table.add_row([customer, f"{order} x {coffee_name}"])
            else:
               print("Error: No item found with the specified price.")
         else:
            order_str = ", ".join([f"{coffee}: {quantity}" for coffee, quantity in order.items()])
            orders_table.add_row([customer, order_str])
      print("All Orders")
      print(orders_table)


coffee_shop = CoffeeShop()
coffee_shop.register()
coffee_shop.login_screen()

while True:
   coffee_shop.display_main_menu()
   choice = input("Enter your choice: ")

   if choice == '1':
      coffee_shop.display_menu_and_stock()
   elif choice == '2':
      coffee_shop.update_menu_and_stock()
   elif choice == '3':
      coffee_shop.delete_menu()
   elif choice == '4':
      coffee_shop.display_menu_and_stock()
      customer_name = input("Enter your name: ")
      coffee = input("Enter the coffee that been ordered : ")
      quantity = int(input("Enter the quantity: "))
      if coffee in coffee_shop.items and coffee_shop.items[coffee]["stock"] >= quantity:
         total_bill = coffee_shop.items[coffee]["price"] * quantity
         coffee_shop.place_order(customer_name, coffee, quantity)
         print(f"Order placed successfully. Total Bill: Rp. {total_bill:.2f}")
         coffee_shop.items[coffee]["stock"] -= quantity
         coffee_shop.generate_invoice(customer_name, {coffee: quantity}, total_bill)
         coffee_shop.total_income += total_bill 
      else:
         print("Invalid coffee selection or insufficient stock.")
   elif choice == '5':
      coffee_shop.display_orders() 
   elif choice == '6':
      coffee_shop.display_total_income() 
   elif choice == '7':
      print("Thank you for using the Coffee Shop system.")
      break
   else:
      print("Invalid choice. Please try again.")
