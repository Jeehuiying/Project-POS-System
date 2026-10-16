"""
Name:Coupon Module

What it contains: Coupon details like coupon ID, coupon created date,
coupon expired date and discount amount. In addition, it also included
function like:
1. Validate the coupon status
2. Mark used coupon so that coupon can only use once
3. Generate coupon with admin input discount amount
4. Print coupon details

Created by: Loh Zhi Yun
"""

from datetime import date, datetime, timedelta
import random

class Coupon:

    coupons = {}

    def __init__(self, couponID, createdDate:date, expiryDate:date, discountAmount: float):
        self.couponID = couponID
        self.createdDate = createdDate
        self.expiryDate = expiryDate
        self.discountAmount = discountAmount
        self.__status = True # True = valid, False = invalid

    def isValid(self) -> bool:
        print("\nChecking validity of coupon ... ...\n")
        now = datetime.now().date()

        if self.__status and now <= self.expiryDate :
            print (f"Coupon {self.couponID} is valid")
            return True
        elif now > self.expiryDate :
            print (f"Coupon {self.couponID} is expired\n")
            return False
        else: #  self.__status = False (Coupon is used)
            print (f"Invalid coupon, coupon has been used. \n")
            return False

    def markAsUsed(self):
        self.__status = False
        return self.__status

    def generateCouponDetails(self):
        while True: # a 6 digit coupon ID is random generate without duplicate with preset data
            cid = str(random.randint(100000, 999999))
            if cid not in Coupon.coupons:
                self.couponID = cid
                break
        self.createdDate = datetime.now().date() # create a date, now is refer to execution date
        self.expiryDate = self.createdDate + timedelta(days=60) # coupon only valid within 60 days

        while True:
            try:
                self.discountAmount = float(input("Enter discount amount: RM "))
                if self.discountAmount > 0:
                    break
                else:
                    print("Invalid discount amount")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")


        return {
            "couponID": self.couponID,
            "createdDate": self.createdDate,
            "expiryDate": self.expiryDate,
            "discountAmount": self.discountAmount
        }

    def printCoupon(self):
        print ("\n")
        print ("=" * 41)
        print ('            SE 光明未来 STORE          ')
        print ("=" * 41)
        print (f' Coupon ID        : {self.couponID} ')
        print (f' Created Date     : {self.createdDate} ')
        print (f' Expiry Date      : {self.expiryDate} ')
        print ("=" * 41)
        print (f' Discount Amount   : RM {self.discountAmount} ')
        print ("=" * 41)
        print("\n")







