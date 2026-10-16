"""
Name: Payment Module

Takes after Inventory System after updating the stocks and computing the total amount.
Focused on the method of payments which is cash, check and credit card.

Created by Estherne Liow Ker Yin
"""
from datetime import datetime, timedelta
from authentication import Authentication

class Payment:
    def __init__(self, amount, currency="RM", status= False):
        self.amount = amount
        self.currency = currency
        self.status = status

    def payment_process(self):
        raise NotImplementedError("Subclass: Check, Cash, CreditCard")
         
    def hasPaid(self):
            print("=" * 30)
            print (f"{self.currency}{self.amount} has been paid.\n")
            print("=" * 30)
            self.status = True
    
    def print_amount(self):
         print (f"Total amount is {self.currency}{self.amount}")

    def check_status(self):
         state = "Paid" if self.status else "Unpaid"
         print(f"Payment Status: {state}")

class CreditCard(Payment):

    def __init__(self, amount, currency, card_number, expiry_date, card_type):
       super().__init__(amount, currency)

       self.__card_number = str(card_number)
       self.__expiry_date = expiry_date  # read by card reader
       self.__card_type = card_type # VISA / MasterCard

    def payment_process(self, card_number=None, card_type=None, expiry_date=None):
        """
        Overloaded method:
        Can pass card_number, card_type, expiry_date directly instead of using stored ones.
        """
        if card_number: self.__card_number = str(card_number)
        if card_type: self.__card_type = card_type
        if expiry_date: self.__expiry_date = expiry_date

        if self.is_card_expired():
            return "Payment failed: Card is expired."
        return f"Processing {self.__card_type} credit card payment of {self.currency}{self.amount:.2f}..."

    # ---------------------
    @property
    def card_number(self):
        return f"**** **** **** {self.__card_number[-4:]}"  #secure payment ,only display last 4 digits

    @property
    def card_type(self):
        return self.__card_type

    def is_card_expired(self):
        return datetime.now().date() > self.__expiry_date



class Cash(Payment):
    def __init__(self, amount, currency):
        super().__init__(amount, currency)
        self.customer_amount = 0.0      # Amount provided by customer
        self.__change = 0.0               # Change to return
        self.denominations = {}        # Denominations given by the customer

    def record_denominations(self):
        remaining = self.customer_amount
        self.denominations = {}
        for bill in [100, 50, 20, 10, 5, 1]:
            count = remaining // bill
            if count > 0:
                self.denominations[bill] = count
                remaining -= bill * count

    def payment_process(self, customer_amount=None):
        """
        Overloaded method:
        If customer_amount provided, use it directly;
        otherwise, prompt input from user.
        """
        if customer_amount is None:
            while True:
                try:
                    customer_amount = float(input(f"Customer's amount ({self.currency}): "))
                    if check_amount(self.amount, customer_amount):
                        break
                    else:
                        print("Amount is not enough. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        self.customer_amount = customer_amount
        self.record_denominations()
        self.__change = remainder(self.amount, self.customer_amount)
        print(f"Change: {self.currency}{self.__change:.2f}")
        return f"Processing cash payment of {self.currency}{self.amount:.2f}..."

    def get_change(self):
        """Return the calculated change"""
        return self.__change

    def get_denominations(self):
        """Return the denominations provided by the customer"""
        return self.denominations



class Check(Payment):
    def __init__(self, amount, currency, check_number, payer_name, account_number, bank_name, date):
        super().__init__(amount, currency)
        self.check_number = check_number
        self.payer_name = payer_name
        self.bank_name = bank_name
        self.__account_number = account_number
        self.date = date
    
    def is_Check_valid(self):
        date_now = datetime.now()
        check_date = self.date
        if check_date < (date_now - timedelta(days=180)):
            print ("Check is expired. Please enter another check.")
            return False
        else:
            return True
        
    def show_check_info(self):
        print(f"Check number: {self.check_number}")
        print(f"Payer's name: {self.payer_name}")
        print(f"Bank name   : {self.bank_name}")
        print(f"Account number:{self.get_account_number()}")
        print(f"Check date   : {self.date}")

    def get_account_number(self):
        return self.__account_number

    def payment_process(self, check_number=None):
        """Overloaded method: can provide a new check number"""
        if check_number:
            self.check_number = check_number
        return f"Processing check number {self.check_number} payment of {self.currency}{self.amount:.2f}..."





#payment related functions
def pay(amount, cashierID, productList):
    from receipt import Receipt
    import receipt

    print("=" * 41)
    print(" " * 14 + "PAYMENT METHOD" + " " * 13)
    print("=" * 41)
    print ("1. Cash")
    print ("2. Check")
    print ("3. Credit Card")
    print("=" * 41)
    payment_method = int(input("Select payment process:"))

    if (payment_method == 1):
        ca = Cash(amount, "RM")
        print(ca.payment_process())
        ca.hasPaid()
        ca.check_status()
        customer_change = ca.get_change()

    elif (payment_method == 2):
        check_number = "0"
        loopch = False
        date = 0
        account_number = 0
        while not loopch:
           while len(check_number)< 3 or len(check_number)> 6 or not Authentication.is_valid_number(check_number):
             check_number = input("Please insert the valid check number (3-6 digits):")

           while True:  
               date = input("Please enter check date (YYYY-MM-DD):")
               try:
                  date_object = datetime.strptime(date, "%Y-%m-%d")
                  break
               except ValueError:
                  print("Wrong format. Please insert the correct date: (2025-12-25)")
           
           payer_name = input("Please enter payer's name:")
           bank_name = input("Please enter Bank's name:")
           while True:
               account_number = input("Please enter the account number (10-16 digits): ").strip()
               if account_number.isdigit() and 10 <= len(account_number) <= 16:
                   break
               else:
                   print("Invalid account number. It must be 10-16 digits.")

           ch = Check(amount,"RM", check_number, payer_name, account_number, bank_name, date_object)
           if ch.is_Check_valid()  :
             loopch = True

           else:
             check_number="0"

        ch.show_check_info()
        print(ch.payment_process())
        ch.hasPaid()
        ch.check_status()
        customer_change = 0
        print("Check details have been successfully recorded into log book")
   
    elif (payment_method == 3):
        card_number = ""
        loopcc = False

        # Loop until a valid and non-expired credit card is entered
        while not loopcc:
            # Prompt user to enter a valid 16-digit credit card number
            while len(card_number) != 16 or not card_number.isdigit():
                card_number = input("Enter valid 16-digit credit card number (no '-'): ")

            # Let cashier select the card type (VISA or MasterCard)
            while True:
                print("Select card type:")
                print("1. VISA")
                print("2. MasterCard")
                card_type_choice = input("Enter choice (1-2): ")

                if card_type_choice == "1":
                    card_type = "VISA"
                    break
                elif card_type_choice == "2":
                    card_type = "MasterCard"
                    break
                else:
                    print("Invalid choice, please enter 1 for VISA or 2 for MasterCard\n")

            print(f"Selected card type: {card_type}")

            # Set the expiry date (simulating a system read / future date for testing)
            expiry_date = datetime.strptime("12/26", "%m/%y").date()

            # Create a CreditCard object with the provided details
            cc = CreditCard(amount, "RM", card_number, expiry_date, card_type)

            # Check if the card is expired
            if cc.is_card_expired():
                print("Card expired. Please try another card.")
                card_number = ""  # Reset card number to retry
            else:
                loopcc = True  # Exit loop if card is valid and not expired

        # Display payment information
        print(f"Card Number: {cc.card_number}")  # Masked card number
        print(f"{cc.payment_process()}")  # Process payment message
        cc.hasPaid()  # Mark payment as completed
        cc.check_status()  # Show payment status
        customer_change = 0  # No change for card payments


    elif not Authentication.is_valid_number(payment_method):
        print("Invalid input. Please enter 1-3")
    
    else:
        print("Invalid input. Please enter 1-3")

    rec = Receipt(amount, cashierID, productList, customer_change)
    rec.generate_receipt()
    receipt.addReceipt(rec)


def check_amount(amount, customer_amount):
    if customer_amount < amount:
        return False
    return True


def remainder(amount, customer_amount):
    if customer_amount < amount:
        return 0
    return customer_amount - amount
