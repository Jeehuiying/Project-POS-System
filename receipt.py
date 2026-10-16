"""
Name: Receipt Module

This module basically is used to generate and print receipt.

Created by: Leong Jao Yuan
"""
import random
import datetime

class Receipt:
    def __init__(self, amount, cashierID, productList, customer_change):
        self.amount = amount
        self.cashierID = cashierID
        self.productList = productList   # dict from Sales
        self.customer_change = customer_change
        self.receiptID = random.randint(1000, 9999)
        self.datetime = datetime.datetime.now()
        self.isReturnable=True # valid to return when True, False is unreturnable
    
    def getDate(self):
        return self.datetime.date()

    #a receipt can only be used for one return
    def markAsReturned(self):
        self.isReturnable=False

    def generate_receipt(self):
        print ("\n")
        print("=" * 41)
        print ('            SE 光明未来 STORE          ')
        print ("=" * 41)
        print(f"Receipt ID: {self.receiptID}")
        print(f"Cashier ID: {self.cashierID}")
        print (f"Time      : {self.datetime}")
        print ("=" * 16 + " Receipt " + "=" * 16)
        for item in self.productList.values():
            subtotal = item['price'] * item['qty']
            print(
                f"{item['name']:<20} x{item['qty']:<3}"
                f" RM{subtotal:>7.2f}"
            )
        print ("=" * 41)
        print(f"{'Total     :':<25} RM{float(self.amount):>7.2f}")
        print(f"{'Change    :':<25} RM{float(self.customer_change):>7.2f}")
        print("=" * 41)
        print("\n\n")

#list to store created receipts
receiptList = []
#methods to search for receipts
def addReceipt(receipt):
    receiptList.append(receipt)

def searchReceipt(receiptID):
    for receipt in receiptList:
        if str(receipt.receiptID) == receiptID:
            return receipt
    return None