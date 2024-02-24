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
      self.loggedInUser = None
      self.customerName = None
      self.total_income = 0 

   def displayMenuAndStock(self):
      table = PrettyTable(["Menu", "Price", "Stock"])
      for item, info in self.items.items():
            table.add_row([item, info["price"], info["stock"]])
      print("Coffee Shop Menu and Stock")
      print(table)

   def updateMenuAndStock(self):
      self.displayMenuAndStock()
      item = input("Enter the item to update: ")
      if item in self.items:
            price = int(input("Enter the new price: "))
            quantity = int(input("Enter the new stock quantity: "))
            self.items[item]["price"] = price
            self.items[item]["stock"] = quantity
            print(f"Menu item '{item}' updated successfully.")
      else:
            print(f"Menu item '{item}' not found.")

   def deleteMenu(self):
      self.displayMenuAndStock()
      item = input("Enter the item to delete: ")
      if item in self.items:
            del self.items[item]
            print(f"Menu item '{item}' deleted successfully.")
      else:
            print(f"Menu item '{item}' not found.")

   def placeOrder(self, customerName, coffeeName, quantity):
      if customerName in self.orders:
         if coffeeName in self.orders[customerName]:
            self.orders[customerName][coffeeName] += quantity
         else:
            self.orders[customerName][coffeeName] = quantity
      else:
         self.orders[customerName] = {coffeeName: quantity}


   def registerUser(self, username, password):
      if username not in self.users:
            self.users[username] = {"password": password, "role": "customer", "balance": 0}
            print("Registration successful.")
      else:
            print("Username already exists. Please choose another username.")

   def login(self, username, password):
      if username in self.users and self.users[username]["password"] == password:
            self.loggedInUser = username
            return True
      return False

   def invoices(self, customerName, customerOrder, totalBill):
      with open(f'{customerName}_invoice.txt', 'w') as invoice:
            invoice.write("CoffeeShop Invoice\n")
            invoice.write(f"Customer Name: {customerName}\n")
            for coffee, quantity in customerOrder.items():
               invoice.write(f"{coffee}: {quantity}\n")
            invoice.write(f"Total Bill: Rp. {totalBill:.2f}\n")

   def generateInvoice(self, customerName, customerOrder, totalBill):
      invoice = PrettyTable()
      invoice.field_names = ["CoffeeShop", "Invoice"]
      invoice.add_row(["Customer Name:", customerName])
      invoice.add_row(["Transaction Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
      for coffee, quantity in customerOrder.items():
            invoice.add_row([coffee, f"{quantity}"])
      invoice.add_row(["Total Bill:", f"Rp. {totalBill:.2f}"])
      print(invoice)
      self.invoices(customerName, customerOrder, totalBill)

   def register(self):
      print("Welcome To Coffee Shop \nPlease Register First❤️")
      username = input("Enter your username: ")
      password = input("Enter your password: ")
      self.registerUser(username, password)

   def loginScreen(self):
      while True:
            print("Login Your Account✌️")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if self.login(username, password):
               print(f"Welcome, {username}!")
               break
            else:
               print("Invalid username or password. Please try again.")

   def displayMainMenu(self):
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

   def displayTotalIncome(self):
      print(f"Total Income: Rp. {self.total_income}")

   def displayOrders(self):
      orders_table = PrettyTable(["Customer Name", "Order"])
      for customer, order in self.orders.items():
         if isinstance(order, int):
            coffeeName = None
            for coffee, info in self.items.items():
               if info["price"] == order:
                  coffeeName = coffee
                  break
            if coffeeName:
               orders_table.add_row([customer, f"{order} x {coffeeName}"])
            else:
               print("Error: No item found with the specified price.")
         else:
            order_str = ", ".join([f"{coffee}: {quantity}" for coffee, quantity in order.items()])
            orders_table.add_row([customer, order_str])
      print("All Orders")
      print(orders_table)


coffee_shop = CoffeeShop()
coffee_shop.register()
coffee_shop.loginScreen()

while True:
   coffee_shop.displayMainMenu()
   choice = input("Enter your choice: ")

   if choice == '1':
      coffee_shop.displayMenuAndStock()
   elif choice == '2':
      coffee_shop.updateMenuAndStock()
   elif choice == '3':
      coffee_shop.deleteMenu()
   elif choice == '4':
      coffee_shop.displayMenuAndStock()
      customerName = input("Enter your name: ")
      coffee = input("Enter the coffee that been ordered : ")
      quantity = int(input("Enter the quantity: "))
      if coffee in coffee_shop.items and coffee_shop.items[coffee]["stock"] >= quantity:
         totalBill = coffee_shop.items[coffee]["price"] * quantity
         coffee_shop.placeOrder(customerName, coffee, quantity)
         print(f"Order placed successfully. Total Bill: Rp. {totalBill:.2f}")
         coffee_shop.items[coffee]["stock"] -= quantity
         coffee_shop.generateInvoice(customerName, {coffee: quantity}, totalBill)
         coffee_shop.total_income += totalBill 
      else:
         print("Invalid coffee selection or insufficient stock.")
   elif choice == '5':
      coffee_shop.displayOrders() 
   elif choice == '6':
      coffee_shop.displayTotalIncome() 
   elif choice == '7':
      print("Thank you for using the Coffee Shop system.")
      break
   else:
      print("Invalid choice. Please try again.")
