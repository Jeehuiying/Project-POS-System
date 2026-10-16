"""
Name: Sales Module

What it contains:
It contains the Sales class, which stores sales information
such as the sales date and time, total amount, product count,
and discount amount during the checkout process.

Created by:Jee Hui Ying
"""

import random
from datetime import datetime
from Coupon import Coupon
from authentication import Authentication


class Sales:
    def __init__(self):
        self.__salesID=None
        self.salesDateTime=None
        self.totalAmount=0
        self.productCount=0
        self.discountAmount=0
        self.productlist = {}

    def generateSalesID(self):
        self.__salesID=random.randint(100000, 999999);   #generate a random salesID
        return self.__salesID

    def get_DateTime(self):
        self.salesDateTime=datetime.now()
        return self.salesDateTime

    def add_product(self, barcode, product):
        if barcode in self.productlist:
            self.productlist[barcode]['qty'] += 1
        else:
            self.productlist[barcode] = {
                'name': product['name'],
                'price': product['price'],
                'qty': 1
            }

        print(f"{product['name']} x{self.productlist[barcode]['qty']} - RM{product['price']:.2f}")


    def get_products(self):
        return self.productlist

    def compute_total_amount(self,product):
        self.totalAmount += product['price']


    def compute_product_count(self):
        self.productCount += 1
        return self.productCount

    def getDiscountAmount(self):
      discount = 0
      while True:
        couponID=input("\nEnter coupon ID(E to exit): ")
        c = Coupon.coupons.get(couponID)

        if c:
            if not Authentication.is_valid_number(couponID):
                print("PLease enter a digit number\n")
                continue
            elif c.isValid(): # check whether coupon is valid before apply (avoid reuse of coupon)
                discount = c.discountAmount
                c.markAsUsed() # mark coupon as used, coupon is invalid after marked
                print("Voucher Applied!")
                print(f"Total Discount Amount: RM {discount:.2f}")
                break
            else:
                print("Coupon is not valid.")
                discount = 0

        elif couponID=="E" or  couponID=="e":
            break
        else:
            print("Coupon not found.")
            discount = 0

      self.discountAmount = discount
      return self.discountAmount

    #overloading method
    #show_total_amount() to display total price before discount
    #show_total_amount(discount) to display total price after discount
    def show_total_amount(self, discount=None):

        #Total price before discount
        if discount is None:
            return self.totalAmount

        else:
            #Total price after discount
            total_after_discount = self.totalAmount - discount

            if total_after_discount < 0:
                total_after_discount = 0

            return total_after_discount
