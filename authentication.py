"""
Name: Authentication Module

What it contains:
It contains the Authentication class which provides functions for
user authentication, password validation, phone number validation,
and station checking for administrators and cashiers.

Created by:Lim Gek Hong
"""

from users import Administrator
from users import Cashier



class Authentication:

    def __init__(self):
        self.__system_name = "AuthenticationModule"
        self.__version = "4.0"
        self.__author = "System"

    def get_authenticator_info(self):
        return f"Authentication system name:{self.__system_name}\nVersion:{self.__version}\nAuthor:{self.__author}"

    def match_check_admin_id(self, user_id):
        return user_id in Administrator.get_admin_dic()

    def check_admin_password(self,user_id,user_password):
        return Administrator.admin_dic[user_id]["password"]==user_password

    def match_check_cashier_id(self, user_id):
        return user_id in Cashier.get_cashier_dic()

    def check_cashier_password(self, user_id, user_password):
        info = Cashier.cashier_dic.get(user_id)
        if not info:
            return False
        return info["password"] == user_password

    @staticmethod
    def validate_string(password):  #validate password(must be at least on big capital character and one special character)
        if len(password) > 15:
            return False

        has_letter = any(ch.isalpha() for ch in password)
        has_special = any(not ch.isalnum() for ch in password)
        has_uppercase = any(ch.isupper() for ch in password)

        return has_letter and has_special and has_uppercase

    @staticmethod
    def validate_malaysia_phone(number):
        # Check if the input contains only digits (no dash, no space, no letters)
        if not number.isdigit():
            return False

        # malaysian mobile numbers usually start with "01"
        # all mobile prefixes fall under 010 – 019
        if not number.startswith("01"):
            return False

        # malaysian local mobile numbers are usually 10 or 11 digits long like:
        # 0101234567   change to 10 digits
        # 01112345678  change to 11 digits
        length = len(number)
        if length == 10 or length == 11:
            return True

        # return False if the length is not valid
        return False
    @staticmethod
    def is_station_taken(station):
        for info in Cashier.cashier_dic.values():
            if info["station"] == station:
                return True
        return False

    @staticmethod
    def is_valid_number(value):
        return value.isdigit()

    @staticmethod
    def is_in_range(value, min_value, max_value):
        return min_value <= value <= max_value

    @staticmethod
    def validate_cashier_id(cashier_id):
        # must start with CSH
        if not cashier_id.startswith("csh"):
            return False

        number_part = cashier_id[3:]

        # must be exactly 10 digits
        if not number_part.isdigit() or len(number_part) != 10:
            return False

        return True
