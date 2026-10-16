"""
Name:Users module

It contains 5 preset administrator records:
 Admin ID       | password
 -------------------------------
"adm1000000001": "7877hd#Jidnj"-------------owner(super-admin)
"adm1000000002": "27837hDybdj@"
"adm1000000003": "bDHg783790&&o"
"adm1000000004": "988999F900#"
"adm1000000005": "888hHHHhhhji*"

 adm1000000001: 7877hd#Jidnj is the owner of the shop ,the other are just normal admin(manager), she is the person only
 who allowed to add in new administrator(manager)

 with 5 preset cashier records also:
  "csh1000000001": "392024iWj2@@" --station 1
  "csh1000000002": "0099993%Fj*#" --station 2
  "csh1000000003":"929485huEh&"-- station 3
  "csh1000000004":"adjD3059###"--station 4
  "csh1000000005":"i9i9Dbjwhu**"--station 5

  It contains the user base class and its subclasses Cashier, Administrator,
  and SuperAdministrator.This module manages user data and user-related
  operations in the system.

Created by: Lim Gek Hong
"""
import random
from abc import ABC, abstractmethod


#abstract class because it only represents a general concept
class User(ABC):

    def __init__(self,user_password,user_name,user_role,contact_number):


        self._user_name = user_name
        self._password = user_password
        self._role=user_role
        self._contact_number=contact_number


    @property
    def user(self):
        return self._user_name

    @property
    def role(self):
        return self._role

    #override
    @staticmethod
    @abstractmethod
    def generate_ids():
        """Generate a unique user ID"""
        pass

class Cashier(User):

    # one class attribute
    cashier_dic = {
        "csh1000000001": {
            "password": "392024iWj2@@",
            "user_name": "Ali bin Abu",
            "role": "Cashier",
            "contact": "0123456789",
            "station": 1
        },
        "csh1000000002": {
            "password": "0099993%Fj*#",
            "user_name": "Aisyah",
            "role": "Cashier",
            "contact": "0139876543",
            "station": 2
        },
        "csh1000000003": {
            "password": "929485huEh&",
            "user_name": "Jason Tan",
            "role": "Cashier",
            "contact": "0142223333",
            "station": 3
        },
        "csh1000000004": {
            "password": "adjD3059###",
            "user_name": "Nur Aina",
            "role": "Cashier",
            "contact": "0165556666",
            "station": 4
        },
        "csh1000000005": {
            "password": "i9i9Dbjwhu**",
            "user_name": "Kevin Ong",
            "role": "Cashier",
            "contact": "0178889999",
            "station": 5
        }
    }

    def __init__(self, user_password,user_name,  contact_number, station,cashier_id):
                super().__init__( user_password,user_name, "Cashier", contact_number)
                self.__station = station
                self.__cashier_id=cashier_id

    @staticmethod
    def get_cashier_dic():
            return Cashier.cashier_dic

    # override
    @staticmethod
    def generate_ids():
          # keep generating a new cashier id until a unique one is found
          while True:
            # generate a random 10 digit number and add "CSH" prefix
            cid = "csh" + str(random.randint(10 ** 9, 10 ** 10 - 1))

            # check if the generated id are already exists
            if cid not in Cashier.cashier_dic:
                return cid  # return the unique cashier id

    @staticmethod
    def scanBarcode():
        return input("Barcode Number : ")



#admin class inherits from user
class Administrator(User):
    # class attribute
    admin_dic = {
        "adm1000000001": {
            "password": "7877hd#Jidnj",  #owner of the store
            "user_name": "Lim Gek Hong",
            "role": "Super Administrator",
            "contact": "0123456789"
        },
        "adm1000000002": {
            "password": "27837hDybdj@",
            "user_name": "Estherne Liow Ker Yin",
            "role": "Administrator",
            "contact": "0134567890"
        },
        "adm1000000003": {
            "password": "bDHg783790&&o",
            "user_name": "Jee Hui Ying",
            "role": "Administrator",
            "contact": "0145678901"
        },
        "adm1000000004": {
            "password": "988999F900#",
            "user_name": "Leong Jao Yuan",
            "role": "Administrator",
            "contact": "0156789012"
        },
        "adm1000000005": {
            "password": "888hHHHhhhji*",
            "user_name": "Loh Zhi Yun",
            "role": "Administrator",
            "contact": "0167890123"
        }
    }# dictionary is mutable,so it is easier to append new admin later


    def __init__(self, user_password, admin_id):
        super().__init__(user_password,user_name=None, user_role="Administrator",contact_number=None) #in order to reuse the constructor of the parent class and avoid code duplication
        self.__admin_id = admin_id
        self.__level = "NORMAL" #system assigns a default level of NORMAL to newly created administrators


    @staticmethod
    def get_admin_dic():
        return Administrator.admin_dic


    def add_cashier(self):
        from authentication import Authentication
        # display suggested cashier IDs for user convenience
        print("\nSuggested Cashier IDs:")

        # generate 3 unique cashier id suggestions
        suggestions = [Cashier.generate_ids() for _ in range(3)]

        # print each suggested id
        for s in suggestions:
            print(s)

        print("\n")
        # allow user to enter their own id or press Enter to use the first suggestion
        while True:
            new_id = input("Enter cashier ID (or press Enter to use first suggestion): ").strip()

            if new_id == "":
                new_id = suggestions[0]
                break

            if not Authentication.validate_cashier_id(new_id):
                print("Invalid cashier ID format, the format should be CSH followed by 10 digits number, please re-enter\n")
                continue

            if new_id in Cashier.cashier_dic:
                print("Duplicate cashier ID, please enter another ID\n")
                continue

            break

        #prompt admin to enter new added cashier's name and phone number
        name = input("Enter name：")

        while True:
            contact_num = input("Enter contact number:")
            from authentication import Authentication
            if Authentication.validate_malaysia_phone(contact_num):
                break
            else:
                print("Invalid contact number format, please enter again\n")

        station = None

        while True:
            try:
                temp = int(input("Enter cashier station (e.g. Station 1 then press 1): "))
                station = temp

                if station <= 0:
                    print("Station number must be a positive number\n")
                    continue

                if Authentication.is_station_taken(station):
                    print(f"Station {station} has already been taken, please choose another station\n")
                    continue

                break

            except ValueError:
                print("Invalid input, please enter a number\n")

        if station is None:
            print("Station not set")
            return
        # prompt user to enter password for the new cashier
        while True:
          password = input("Key in cashier password: ")
          if len(password)>8 and Authentication.validate_string(password):
            #add new cashier account into the cashier dictionary
            Cashier.cashier_dic[new_id] = {
                "password": password,
                "user_name":name,
                "role": "Cashier",
                "contact": contact_num,
                "station": station
            }
            print(f"Cashier {new_id} added successfully")
            break
          else:
              print("Invalid input, please enter a password with length >8 and <16, and at least one special character + uppercase")
    #override
    @staticmethod
    def generate_ids():
        # generate a unique administrator ID
        while True:
            aid = "adm" + str(random.randint(10 ** 9, 10 ** 10 - 1))
            if aid not in Administrator.admin_dic:
                return aid


    def update_cashier(self):

        # check if cashier dictionary is empty
        if not Cashier.cashier_dic:
            print("No cashier record to update.")
            return

        self.view_cashier()

        total_records = len(Cashier.cashier_dic)

        while True:
            record_num = input("Which record would you like to update? (e.g: 1): ")

            # check digit
            from authentication import Authentication
            if not Authentication.is_valid_number(record_num):
                print("Please enter a valid number\n")
                continue

            record_num = int(record_num)

            # check range
            if not Authentication.is_in_range(record_num, 1, total_records):
                print(f"Enter a number between 1 and {total_records}\n")
                continue


            break
        cashier_ids = list(Cashier.cashier_dic.keys())
        selected_cashier_id = cashier_ids[record_num - 1]

        print(f"You selected Cashier ID: {selected_cashier_id} with record {record_num}")
        print("Cashier details:", Cashier.cashier_dic[selected_cashier_id])


        # Next step: choose attribute to update
        print("=" * 41)
        print("  Which attribute do you want to modify?")
        print("=" * 41)
        print(" 1. Password\n 2. User Name\n 3. Upgrade to Administrator\n 4. Contact Number\n 5. Station")
        #id is unique cannot simply change it
        while True:
            attr = input("Which attribute would you like to update?: ").strip()

            if not Authentication.is_valid_number(attr):
                print("Please enter a valid number.\n")
                continue

            attr = int(attr)

            if not Authentication.is_in_range(attr, 1, 5):
                print("Please enter a number between 1 and 5\n")
                continue

            break

        match attr:
            case 1:

                while True:
                    new_password = input("Enter new password:")
                    if Authentication.validate_string(new_password):
                        Cashier.cashier_dic[selected_cashier_id]["password"]=new_password
                        break
                    else:
                        print("Please enter a valid password with length >8 and <16 and at least one special character + one uppercase\n")
            case 2:
                new_user_name=input("Enter new user name:")
                Cashier.cashier_dic[selected_cashier_id]["user_name"] = new_user_name
            case 3:

                cashier_info = Cashier.cashier_dic[selected_cashier_id]


                Administrator.admin_dic[selected_cashier_id] = {
                    "password": cashier_info["password"],
                    "user_name": cashier_info["user_name"],
                    "role": "Administrator",
                    "contact": cashier_info["contact"]
                }


                del Cashier.cashier_dic[selected_cashier_id]

                print(f"Cashier {selected_cashier_id} upgraded to Administrator successfully.")

            case 4:

                while True:
                 new_phone_num = input("Enter new contact number:")
                 if Authentication.validate_malaysia_phone(new_phone_num):
                   Cashier.cashier_dic[selected_cashier_id]["contact"] = new_phone_num
                   break
                 else:
                   print("Please enter a valid Malaysian phone number format\n")

            case 5:
                while True:
                 try:
                     new_station = int(input("Enter new station: "))

                     if new_station <= 0:
                       print("Station number must be a positive number\n")
                       continue

                     if Authentication.is_station_taken(new_station):
                       print("Station already taken, choose another\n")
                       continue

                     Cashier.cashier_dic[selected_cashier_id]["station"] = new_station
                     print("Station updated successfully")
                     break

                 except ValueError:
                    print("Please enter a valid number\n")

        print(f"{selected_cashier_id} updated successfully\n")


    def delete_cashier(self):
        # check if cashier dictionary is empty
        if not Cashier.cashier_dic:
            print("No cashier record to delete")
            return

        # display cashier list
        self.view_cashier()

        total_records = len(Cashier.cashier_dic)

        # select record number
        while True:
            record_num = input("Which cashier record would you like to delete?: ")
            from authentication import Authentication
            if not Authentication.is_valid_number(record_num):
                print("Please enter a valid number\n")
                continue

            record_num = int(record_num)

            if not Authentication.is_in_range(record_num, 1, total_records):
                print(f"Enter a number between 1 and {total_records}\n")
                continue

            break

        # map record number to cashier ID
        cashier_ids = list(Cashier.cashier_dic.keys())
        selected_cashier_id = cashier_ids[record_num - 1]

        # delete cashier
        del Cashier.cashier_dic[selected_cashier_id]

        print(f"Cashier {selected_cashier_id} deleted successfully\n")


    def view_cashier(self):
        num=1
        for k, v in Cashier.cashier_dic.items():
            print(f"{num}. Cashier ID: {k}, Details: {v}")
            num+=1
        print("\n")

class SuperAdministrator(Administrator):
    def __init__(self, user_password, admin_id):
        super().__init__(user_password, admin_id)

        self.__access_scope = "FULL"
        self.__founded_year = 2025
        self.__super_admin_name="Lim Gek Hong"

    def view_admin(self):
        num=1
        for k, v in Administrator.admin_dic.items():
            print(f"{num}. Admin ID: {k}, Details: {v}")
            num+=1
        print("\n")

    def delete_admin(self):
        # check if admin dictionary is empty
        if not Administrator.admin_dic:
            print("No admin record to delete")
            return

        # display admin list
        self.view_admin()


        total_records = len(Administrator.admin_dic)

        #select record number
        while True:
            record_num = input("Which admin record would you like to delete?: ")

            if record_num=="1":
                print("You are not allowed delete yourself, please contact technical support if you want to swap your role \n")
                continue
            from authentication import Authentication
            if not Authentication.is_valid_number(record_num):
                print("Please enter a valid number\n")
                continue

            record_num = int(record_num)

            if not Authentication.is_in_range(record_num, 1, total_records):
                print(f"Enter a number between 1 and {total_records}\n")
                continue

            break

        # map record number to admin ID
        admin_ids = list(Administrator.admin_dic.keys())
        selected_admin_id = admin_ids[record_num - 1]

        del Administrator.admin_dic[selected_admin_id]
        print(f"{selected_admin_id} deleted selected_admin_id\n")

    def update_admin(self):

        # check if admin dictionary is empty
        if not Administrator.admin_dic:
            print("No admin record to update")
            return

        # display admin list
        self.view_admin()

        total_records = len(Administrator.admin_dic)

        #select record number
        while True:
            record_num = input("Which admin record would you like to update?: ")
            from authentication import Authentication
            if not Authentication.is_valid_number(record_num):
                print("Please enter a valid number\n")
                continue

            record_num = int(record_num)

            if not Authentication.is_in_range(record_num, 1, total_records):
                print(f"Enter a number between 1 and {total_records}\n")
                continue

            break

        # map record number → admin ID
        admin_ids = list(Administrator.admin_dic.keys())
        selected_admin_id = admin_ids[record_num - 1]

        print(f"\nYou selected Admin ID: {selected_admin_id}")
        print("Admin details:", Administrator.admin_dic[selected_admin_id])

        # choose attribute to update(admin are nor allowed to change to other role)
        print("  Which attribute do you want to modify? ")
        print(" 1. Password\n 2. User Name\n 3. Contact Number")

        while True:
            attr = input("Which attribute would you like to update?: ").strip()

            if not Authentication.is_valid_number(attr):
                print("Please enter a valid number.\n")
                continue

            attr = int(attr)

            if not Authentication.is_in_range(attr, 1, 3):
                print("Please enter a number between 1 and 3\n")
                continue

            break

        #update logic
        match attr:
            case 1:
                while True:
                    new_password = input("Enter new password: ")
                    if Authentication.validate_string(new_password) and len(new_password) > 8:
                        Administrator.admin_dic[selected_admin_id]["password"] = new_password
                        break
                    else:
                        print("Password length must be >8 and <16 characters and contain at least one uppercase + special character\n")

            case 2:
                new_user_name = input("Enter new user name: ")
                Administrator.admin_dic[selected_admin_id]["user_name"] = new_user_name

            case 3:
                while True:
                    new_phone_num = input("Enter new contact number: ")
                    if Authentication.validate_malaysia_phone(new_phone_num):
                        Administrator.admin_dic[selected_admin_id]["contact"] = new_phone_num
                        break
                    else:
                        print("Please enter a valid Malaysian phone number\n")

        print(f"{selected_admin_id} updated successfully\n")


    def add_admin(self):   # function to add new admin by owner ONLY
            print("\n=== Add New Administrator ===")

            # generate new admin ID
            new_id = self.generate_ids()

            print(f"Generated Admin ID: {new_id}")

            new_name = input("Enter admin name: ")

            while True:
                contact = input("Enter contact number: ")
                from authentication import Authentication
                if Authentication.validate_malaysia_phone(contact):
                    break
                print("Invalid contact number, try again")

            while True:
                password = input("Key in admin password: ")
                if len(password) > 8 and Authentication.validate_string(password):
                    break
                print(
                    "Length of password must be more than 8 and less than 16 characters, and password must contain at least one uppercase character + at least one special character")

            # save into admin_dic
            Administrator.admin_dic[new_id] = {
                "password": password,
                "user_name": new_name,
                "role": "Administrator",
                "contact": contact
            }

            print(f"Administrator {new_id} added successfully!\n")






