"""
Name: Return Module

This module The Return module handles product returns by validating receipts,
recording returned items, calculating refunds, updating inventory, and enforcing admin approval.

Created by: Leong Jao Yuan (104742)
"""
from datetime import datetime, timedelta
from authentication import Authentication
import receipt
import random

class Return: 
    def __init__(self):
        self.__returnID=None
        self.__returnDate=None
        self.__returnProducts={}

    @property
    def returnID(self):
        return self.__returnID

    @property
    def returnDate(self):
        return self.__returnDate
    
    @property
    def returnProducts(self):
        return self.__returnProducts
    
    def setReturnDate(self):
        self.__returnDate=datetime.now().date()
       
    def setReturnID(self):
        self.__returnID=random.randint(1000,2000)

    #check if exceeded return period(3 days after receipt generation)
    def isExpired(self, rec):
        return self.__returnDate > rec.getDate() + timedelta(days=3)
   
    def isValidReceipt(self, receiptID):
        rec = receipt.searchReceipt(receiptID)
        #check if receipt id is valid
        if rec is None:
            print("No matches found.")
            return False
        elif not rec.isReturnable:
            print("Receipt not eligible for return.")
            return False
        elif self.isExpired(rec):
            print("Return period has expired.")
        else:
            return True
        
    def isValidProduct(self, barcodeNumber, inv):
        return inv.search_product(barcodeNumber) is not None

    #Overloading method:
    # addReturnProducts(self, receiptProducts, barcode, returnQty): for returnQty>1
    # addReturnProduct(self, receiptProducts, barcode): for returnQty=1
    def addReturnProducts(self, receiptProducts, barcode, returnQty):

        # prevent duplicate barcode
        if barcode in self.returnProducts:
            print("This product has already been returned.")
            return False

        purchasedQty = receiptProducts[barcode]['qty']

        if int(returnQty) <= 0:
            print("Return quantity must be greater than zero.")
            return False
        #return quantity cannot be more than purchased quantity
        elif int(returnQty) > int(purchasedQty):
            print(
                f"Invalid return quantity. "
                f"Purchased: {purchasedQty}, "
                f"Returning Now: {returnQty}"
                )
            return False

        self.returnProducts[barcode] = int(returnQty)
        return True

    def addReturnProduct(self, receiptProducts, barcode):
        return self.addReturnProducts(receiptProducts, barcode, 1)
        
    @staticmethod
    def requestAdminApproval():
        auth=Authentication()
        adminID = input("Administrator ID: ")
        if not auth.match_check_admin_id(adminID):
            print("Invalid administrator ID. Please re-enter your ID.\n")
            return False
        admin_password = input("Password: ")
        if not auth.check_admin_password(adminID, admin_password):
            print("Incorrect password.\n")
            return False
        return True

    def calculateRefundAmount(self, inv):
        refundAmount = 0
        for barcode, qty in self.returnProducts.items():
            product = inv.search_product(barcode)
            refundAmount += product["price"] * qty
        return round(refundAmount, 2)
    
def is_exit(value):
    return (value == "E" or value == "e")
    
#main
def processReturn(ret, inv):
    ret.setReturnDate()
    while True:
        print("=" * 41)
        print(" " * 14 + "HANDLE RETURN" + " " * 14)
        print("=" * 41)
        receiptID=input("Enter receipt ID [E to exit]: ")
        if is_exit(receiptID):
            print("Return process cancelled.")
            return  
        elif not ret.isValidReceipt(receiptID): 
            print("Invalid receipt.")
        else: 
            print("Receipt is valid.")
            break
    rec = receipt.searchReceipt(receiptID)
    
    while True:
        barcodeNumber=input("Enter barcode number of product to return [E to exit, N to proceed to Admin Approval]:")
        if is_exit(barcodeNumber):
            return
        elif barcodeNumber=="N" or barcodeNumber=="n":
            if not ret.returnProducts:
                print("No products selected for return. Cannot proceed.")
                continue
            else:
                break
        elif not ret.isValidProduct(barcodeNumber, inv):
            print("No matches found. Please enter barcode number again.")
            continue
        elif barcodeNumber not in rec.productList:
            print("Product not found in receipt.")
        elif barcodeNumber in ret.returnProducts:
            print("This product has already been returned.")
            continue
        else:
            print("Product can be returned.")
            
            while True:
                returnQty=input("Enter quantity of product to return: ")
                if not Authentication.is_valid_number(returnQty):
                    print ("Invalid input. Please enter a valid number.")
                    break
                if returnQty == "1":
                    success = ret.addReturnProduct(rec.productList, barcodeNumber)
                else:
                    success = ret.addReturnProducts(rec.productList, barcodeNumber, returnQty)

                if success:
                    print("Return item added successfully.")
                    break
                else:
                    print("Failed to add return item. Try again.")
    
    print("\nAdmin approval required for return.")
    chance = 2
    success = False

    while chance > 0:
        if not ret.requestAdminApproval():
            chance -= 1
            print(f"Attempts remaining: {chance}")
        else:
            success = True
            break
    if success:
        print("Return approved by admin.")
        rec.markAsReturned()

        # generate return ID
        ret.setReturnID()

        refundAmount = 0

        for barcode, qty in ret.returnProducts.items():
            product = rec.productList[barcode]
            price = product['price']

            #calculate refund
            refundAmount += price * qty

            #increase inventory stock
            inv.updateStockAmount(barcode, qty)

        print("=" * 41)
        print(" " * 14 + "RETURN RECEIPT" + " " * 13)
        print("=" * 41)
        print(f"Return ID       : {ret.returnID}")
        print(f"Return Date     : {ret.returnDate}")
        print("Returned Products:")
        print("=" * 41)
        print(f"{'Barcode':<15}{'Name':<18}{'Qty':<5}{'Price':<8}")
        for barcode, qty in ret.returnProducts.items():
            product = rec.productList[barcode]
            name = product['name']
            price = product['price']

            print(f"{barcode:<15}{name:<18}{qty:<5}RM{price:.2f}")
        print(f"\nRefund Amount: RM {refundAmount:.2f}")
        print("=" * 41)
        print("Stock updated successfully.")
        print("Return processed successfully.\n")


    else:
        print("Failed to get admin approval. Return cancelled.")
        return
       



        
                
    
        
        

        
    
        
    

    
  
        
  
             
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
