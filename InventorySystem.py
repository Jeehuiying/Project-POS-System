"""
Name: InventorySystem Module

What it contains:
It contains the Inventory class that stores and manages all product data.

Created by:Jee Hui Ying
"""

from users import Cashier
from Sales import Sales
import payment


class InventorySystem:
    def __init__(self,inventoryID):

        self.__inventoryID=inventoryID
        # Predefined product list
        # barcode : {name, price, stock}
        self.__productList = {
            '00009467112': {'name': 'Coke Cola', 'price': 3.50, 'stock': 100, 'expirydate': '2026-11-25'},
            '00004579346': {'name': 'Pepsi', 'price': 3.50, 'stock': 100, 'expirydate': '2026-05-01'},
            '00003934900': {'name': 'Potato Chips', 'price': 2.00, 'stock': 100, 'expirydate': '2026-10-10'},
            '00005200811': {'name': 'Instant Noodles', 'price': 5.50, 'stock': 100, 'expirydate': '2026-12-01'},
            '00006722979': {'name': 'Chili Sauce', 'price': 4.00, 'stock': 100, 'expirydate': '2027-03-11'},
            '00008916407': {'name': 'Milk', 'price': 6.20, 'stock': 100, 'expirydate': '2026-12-30'},
            '00001647035': {'name': 'Cooking Oil', 'price': 28.00, 'stock':50,'expirydate': '2026-10-05'}
        }

        self.__totalStock=0

    def get_inventoryID(self):
        return self.__inventoryID
        
    def search_product(self, barcode):
        return self.__productList.get(barcode)

    #overloading method
    #updateStockAmount(barcode) to decrease stock amount (for scanning process)
    #updateStockAmount(barcode,amount) to increase stock amount (for refunding process)
    def updateStockAmount(self,barcode=None,amount=None):

        prod = self.search_product(barcode)

        if not prod:
            print("Invalid barcode")
            return

        #increase stock amount after refund
        if amount is not None:
            prod['stock'] += amount
    
        #decrease stock amount after scanning barcode
        else:
            if prod['stock'] > 0:
                prod['stock'] -= 1

    def updatePrice(self,barcode,newPrice):
        
        prod = self.search_product(barcode)

        if not prod:
            print("Invalid barcode")
    
        
        else:
            prod['price']=newPrice

    def printAllProducts(self):
        print("=" * 41)
        print(" " * 15 + "PRODUCT LIST" + " " * 14)
        print("=" * 41)
        for barcode, product in self.__productList.items():   
            print(f"Barcode     : {barcode}")
            print(f"Name        : {product['name']}")
            print(f"Price       : RM{product['price']:.2f}")
            print(f"Stock       : {product['stock']}")
            print(f"Expiry Date : {product['expirydate']}")
            print("-" * 35)

    def countTotalStock(self):
        total = 0
        for product in self.__productList.values():
            total += product['stock']
        return total



# ========Main(called by main file)=======

def scanProductProcess(cashierID, inv):
    s=Sales()
    count =0
    print("=" * 41)
    print(" " * 15 + "SCAN PRODUCT" + " " * 14)
    print("=" * 41)
    print("Sales ID:", s.generateSalesID())
    print("Date/Time:", s.get_DateTime())
    print("\nPress N to end")

    while True:
         barcode = Cashier.scanBarcode()
         if barcode.upper() == "N" and count >= 1:
            break
         
         if barcode.upper() == "N" and count <= 0:
            print ("The list is empty. Please insert item.")
            continue

         product = inv.search_product(barcode)

         if product:
            inv.updateStockAmount(barcode)   
            s.add_product(barcode, product)
            s.compute_total_amount(product)
            count=s.compute_product_count()
            print("." * 41)
         else:
            print("Invalid barcode")
      
    print(f"\nTotal Product Numbers : {count}")
    totalprice=s.show_total_amount()
    print(f"\nTotal Amount: RM{totalprice:.2f}\n")

    while True:
        ans=input("Is coupon available? (Y/N) - ")
        if ans =='Y'or ans =='y':
            discount = s.getDiscountAmount()
            totalprice=s.show_total_amount(discount)
            print(f"\nTotal Amount After Discount: RM{totalprice:.2f}\n")
            payment.pay(totalprice, cashierID, s.get_products())
            break
        elif ans == 'N'or ans == 'n':
            print("No Coupon Applied.")
            payment.pay(totalprice, cashierID, s.get_products())
            break
        else:
            print("Invalid input. Please enter Y or N.")
            continue


def InventoryMenu(inv):
    invID=inv.get_inventoryID()
    while True:
        print("=" * 41)
        print(" " * 10 + "INVENTORY SYSTEM MENU" + " " * 10)
        print("=" * 41)
        print(f"Inventory ID : {invID}\n")
        print("1. View All Product Details")
        print("2. Update Product Price")
        print("3. Increase Stock Amount")
        print("4. Decrease Stock Amount")
        print("5. View Total Stock Amount")
        print("6. Back")
        
        choice = input("\nEnter your choice: ")

        if choice == "1":
               inv.printAllProducts()
                                        
        elif choice == "2":
               print("=" * 41)
               print(" " * 11 + "UPDATE PRODUCT PRICE" + " " * 10)
               print("=" * 41)
               bar=input("Enter barcode number of the product: ")
               product = inv.search_product(bar)

               new=eval(input("Enter new price: RM"))
                                        
               if product:
                    inv.updatePrice(bar,new)
                    print("The price has been updated.")
                                                
               else:
                     print("Invalid barcode")
                                            
        elif choice == "3":
               print("=" * 41)
               print(" " * 10 + "INCREASE STOCK AMOUNT" + " " * 10)
               print("=" * 41)
               bar=input("Enter barcode number of the product: ")
               product = inv.search_product(bar)
               num=eval(input("Enter amount to increase: "))
                                        
               if product:
                    inv.updateStockAmount(bar,num)
                    print(f"The stock amount has been increased by {num}.")
                                                
               else:
                    print("Invalid barcode")

        elif choice == "4":
                print("=" * 41)
                print(" " * 10 + "DECREASE STOCK AMOUNT" + " " * 10)
                print("=" * 41)
                bar=input("Enter barcode number of the product: ")
                product = inv.search_product(bar)
                                        
                if product:
                    inv.updateStockAmount(bar)
                    print("The stock amount has been reduced by one.")
                                                
                else:
                    print("Invalid barcode")
                    
        elif choice == "5":
                print("Total Stock:", inv.countTotalStock())

        elif choice == "6":
                print("\nExiting inventory system...")
                break

        else:
                print("Invalid choice. Please select 1-6.")
     
        
