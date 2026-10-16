"""
Name: main module(POS SYSTEM)

What it contains:
This is the entry of POS SYSTEM , so this module also known as POS SYSTEM MODULE
This script handles user login and menu navigation for a POS system.
Supports two roles: Administrator and Cashier.

- Administrator can manage users, issue coupons, and log out.
- Cashier can scan products, view inventory, handle returns, and log out.

Uses:
- Authentication for login validation
- UserManagementUI for admin user management
- Coupon for coupon handling
- InventorySystem and Return for stock and returns management

Created by:All members
"""

from authentication import Authentication
from ManageUser import UserManagementUI
from Coupon import Coupon
from datetime import date
import InventorySystem
import Return
import receipt

inv = InventorySystem.InventorySystem("INVS003")
ret = Return.Return()
#list to store created receipts
receipts=receipt.receiptList

Coupon.coupons = {
    "104762": Coupon("104062", date(2025, 12,12), date(2026,2,12), 25.00),
    "104511": Coupon("104511", date(2025,3, 11), date(2025, 5, 11), 50.00),
    "104742": Coupon("104742", date(2026,1,1), date(2026,3,1), 5.00),
    "104763": Coupon("104763", date(2026,1,15), date(2026,3,15), 15.30),
    "104788": Coupon("104788", date(2025,12,20), date(2026,2,20), 50)
}

auth = Authentication()
logged_in = False
while not logged_in :

 print("=" * 20 + " LOG IN PAGE " + "=" * 20)

 role = input("Select your user role(Administrator(A)/Cashier(C):")

 if role=="administrator" or role=="Administrator" or role=="a" or role=="A":


    loop1 = False
    while not loop1:
       adminID = input("Administrator ID:")
       if auth.match_check_admin_id(adminID):
          loop2=False

          while not loop2:
            admin_password = input("Password:")
            status=auth.check_admin_password(adminID,admin_password)
            if status:
                print(f"Log In Successfully,Welcome {adminID}!\n")

                while True:
                    print("=" * 41)
                    print(" " * 12 + "ADMINISTRATOR MENU" + " " * 11)
                    print("=" * 41)
                    print(" 1. Manage User")
                    print(" 2. Issue Coupon")
                    print(" 3. Log Out\n")
                    print("=" * 35)
                    choice = input("Enter your choice: ")
                    if choice=="1":
                        print("\n")
                        user_management_ui = UserManagementUI(adminID, admin_password)
                        user_management_ui.show_menu()

                    elif choice=="2":
                        newCoupon = Coupon(None, None, None, 0.0)
                        newCoupon.generateCouponDetails()
                        Coupon.coupons[newCoupon.couponID] = newCoupon
                        print("\nNew coupon is generated successfully.")
                        print(f'New Coupon ID: {newCoupon.couponID}')
                        newCoupon.printCoupon()

                    elif choice =="3":
                        print("Log Out Successfully")
                        print(auth.get_authenticator_info())
                        loop2 = True
                        loop1= True
                        logged_in= False
                        break
                    else:
                        print("Invalid choice. Please enter 1-3.\n")


            else:
                print("Incorrect password, please re-enter again.\n")
                loop2=False


       else:
        print("Invalid administrator ID. Please re-enter your ID\n")
        loop1 =False



 elif role=="cashier" or role=="Cashier" or role=="c" or role=="C":
     loop3 = False
     while not loop3:
         cashierID = input("cashier ID:")
         if auth.match_check_cashier_id(cashierID):
             loop2 = False

             while not loop2:
                 cashier_password = input("Password:")
                 status = auth.check_cashier_password(cashierID, cashier_password)
                 if status:
                     print(f"Log In Successfully.Welcome {cashierID}!\n")

                     loop2 = True
                     loop3 = True
                     logged_in = True
                    

                     while True:
                        print("=" * 41)
                        print(" " * 15 + "CASHIER MENU" + " " * 14)
                        print("=" * 41)
                        print(" 1. Scan Products")
                        print(" 2. View Inventory System")
                        print(" 3. Handle Return")
                        print(" 4. Log Out\n")
                        choice = input("Enter your choice: ")

                        if choice == "1":
                            InventorySystem.scanProductProcess(cashierID, inv)

                        elif choice =="2":
                            InventorySystem.InventoryMenu(inv)
                                                        
                        elif choice =="3":
                            Return.processReturn(ret, inv)

                        elif choice =="4":
                            print("Log Out Successfully\n")
                            print(auth.get_authenticator_info())
                            loop2 = True
                            loop3= True
                            logged_in= False
                            break
                        
                        else:
                            print("Invalid choice.\n")

                    
                 else:
                     print("Incorrect password,please re-enter again\n")
                     loop2 = False


         else:
             print("Invalid cashier ID, please re-enter your ID\n")
             loop1 = False

 elif role =="n" or role=="N":
     print("Log Out POS System Successfully")
     print(auth.get_authenticator_info())
     break
 else:
        print("You have entered an invalid role,please enter again(Administrator(A)/Cashier(C)\n")
