"""
Name: User Management UI Module

What it contains:
It contains the UserManagementUI class which provides a command line
interface for administrators and super administrators to manage users,
including viewing, adding, deleting, and updating cashier and administrator
accounts.

Created by:Lim Gek Hong
"""
from users import Administrator, SuperAdministrator

class UserManagementUI:
    current_super_admin = None

    def __init__(self, admin,password):
        self.__current_admin_ID = admin   # current admin(which logged into the system)
        self.__current_password=password
        self.__ui_type = "Command Line Interface"

    def display_logout(self):
        print("Log Out Successfully")

    def menu(self):
        print("=" * 41)
        print(" " * 12 + "MANAGE USER MODULE" + " " * 11)
        print("=" * 41)
        print(" 1. View User\n 2. Add User \n 3. Delete User\n 4. Update User Info\n 5. Exit Manage User Module")


    def show_menu(self):
      if self.__current_admin_ID=="adm1000000001":
          current_super_admin=SuperAdministrator(self.__current_password, self.__current_admin_ID)
          current_admin = current_super_admin
      else:
        current_admin = Administrator(self.__current_password, self.__current_admin_ID)

      while True:

        self.menu()
        choice = input("Please select your choice: ")
        match choice:
            case "1":
                while True:
                   choice2 = input("Do you want to view cashier or administrator(C/A):").strip().upper()
                   if choice2 == "C":
                      current_admin.view_cashier()
                      break
                   elif choice2 == "A" and self.__current_admin_ID == "adm1000000001":
                      current_admin.view_admin()
                      break
                   elif choice2 == "A" and self.__current_admin_ID != "adm1000000001":
                       print("You are not allowed to view admin.\nOnly adm1000000001 is able to view admin.")
                       break
                   else:
                     print("Invalid input, please re-enter your choice(C/A):")
                     continue

            case "2":
              while True:
                    choice2 = input("Do you want to add in new cashier or administrator(C/A):").strip().upper()
                    if choice2 == "C":

                       current_admin.add_cashier()
                       break
                    elif choice2=="A" and self.__current_admin_ID== "adm1000000001" :
                        current_admin.add_admin()
                        break
                    elif choice2 == "A" and self.__current_admin_ID != "adm1000000001":
                        print("You are not allowed to add admin.\nOnly adm1000000001 is able to add admin.")
                        break
                    else:
                        print("Invalid input, please re-enter your choice(C/A):")
                        continue


            case "3":
                while True:
                          choice2 = input("Do you want to delete cashier or administrator(C/A):").strip().upper()
                          if choice2 == "C":
                            current_admin.delete_cashier()
                            break
                          elif choice2 == "A" and self.__current_admin_ID == "adm1000000001":
                            current_admin.delete_admin()
                            break
                          elif choice2 == "A" and self.__current_admin_ID != "adm1000000001":
                              print("You are not allowed to delete admin.\nOnly adm1000000001 is able to delete admin.")
                              break
                          else:
                            print("Invalid input, please re-enter your choice(C/A):")
                            continue
            case "4":
                while True:
                   choice2 = input("Do you want to update cashier or administrator(C/A):").strip().upper()
                   if choice2 == "C":

                        current_admin.update_cashier()
                        break
                   elif choice2 == "A" and self.__current_admin_ID == "adm1000000001":
                        current_admin.update_admin()
                        break
                   elif choice2 == "A" and self.__current_admin_ID != "adm1000000001":
                        print("You are not allowed to update admin info.\nOnly adm1000000001 is able to update admin.")
                        break
                   else:
                        print("Invalid input, please re-enter your choice(C/A):")
                        continue

            case "5":
                self.display_logout()
                break
            case _:
                print("Invalid choice")
                continue


































