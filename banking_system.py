import bcrypt
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class User:
    def __init__(self, name, age, email, password):
        self.name = name
        self.age = age
        self.password = self.hash_password(password)
        self.email = email

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password)
    
    def show_details(self):
        return "Thank you, {} year old, {}".format(self.age, self.name.title())

class Bank(User):
    total_deposits = 0
    total_withdraws = 0

    def __init__(self, name, age, email, balance, password):
        super().__init__(name, age, password, email)
        self.balance = balance

    def show_info(self):
        return f"{self.name} has a remaining balance of: ${round(self.balance, 2)}"

    def deposit(self):
        dp = float(input("{}, please enter how much you would like to deposit: ".format(self.name.title())))
        print("Thank you for depositing")
        self.balance += dp
        self.total_deposits += 1
        return f"Your balance is now: ${round(self.balance, 2)}"

    def withdraws(self):
        wd = float(input("{}, please enter how much you would like to withdraw: ".format(self.name.title())))
        if self.balance < wd:
            return "You can not withdraw that amount"
        else:
            print("Thank you for withdrawing!")
            self.balance -= wd
            self.total_withdraws += 1
            return f"Your balance is now: ${round(self.balance, 2)}"
def send_otp(email):
    otp = random.randint(123456, 987654)
    message = MIMEMultipart()
    message['From'] = 'bcbank@gmail.com'
    message['To'] = email
    message['Subject'] = 'Your OTP Code'
    message.attach(MIMEText(f"Your OTP code is {otp}", 'plain'))


    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 535)
        smtp_server.starttls()
        smtp_server.login('rehmazaidi20021@gmail.com', password)
        smtp_server.sendmail('rehmazaidi20021@gmail.com', email, message.as_string())
        smtp_server.close()
        print("OTP successfuly sent")
    except Exception as e:
        print(f"Error: {str(e)}")

    return otp

def verify_otp(user_otp, actual_otp):
    return user_otp == actual_otp


def options(user_two):
    print("Thank you for creating your bank account")
    print("Here are a list of options, please choose the number you want")
    
    while True:
        option_choice = int(input("1) See Balance\n2) Withdraw\n3) Deposit\n4) See Total Withdraws\n5) See Total Deposits\n6) Quit\n"))
        if option_choice == 1:
            print(user_one_bank.show_info())
            if option_choice == 1 and user_two != None:
                print(user_two_bank.show_info())
        elif option_choice == 2:
            actual_otp = send_otp(user_one_bank.email)
            user_otp = int(input("Enter the OTP sent to your email: "))
            if verify_otp(user_otp, actual_otp):
                print(user_one_bank.withdraws())
                if option_choice == 2 and user_two != None:
                    wd = input(f"{user_two.name}, would you like to withdraw? Yes or No: ")
                    if wd.lower() == 'yes':
                        actual_otp = send_otp(user_two_bank.email)
                        user_otp = int(input("Enter the OTP sent to your email: "))
                        if verify_otp(user_otp, actual_otp):
                            print(user_two_bank.withdraws())
            else:
                print("Invalid OTP")
            
        elif option_choice == 3:
            print(user_one_bank.deposit())
            if option_choice == 3 and user_two != None:
                dep = input(f"{user_two.name} would you like to deposit? Yes or No: ")
                if dep.lower() == 'yes':
                    print(user_two_bank.deposit())
        elif option_choice == 4:
            print(f"There has been {user_one_bank.total_withdraws} withdrawal.")
            if option_choice == 4 and user_two != None:
                print(f"There has been {user_two_bank.total_withdraws} withdrawal.")
        elif option_choice == 5:
            print(f"There has been {user_one_bank.total_deposits} deposits.")
            if option_choice == 5 and user_two != None:
                print(f"There has been {user_two_bank.total_deposits} deposits.")
        elif option_choice == 6:
            print("Thank you for banking with us!")
            return False
            break
        else:
            print("Please choose a number from 1 to 6:")

def bank_creation(name):
    balance = float(input(f"{name.title()}, how much money do you have? "))
    return balance

while True:
    print("Welcome to BC Bank")
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    password = input("Enter your password: ")
    email = input("Enter your email: ")
    user_one = User(name, age, email, password)
    user_two = None
    new_user = input("Would you like to register a new person? Type 'No' to create your bank ")
    if new_user.lower() == 'yes':
        name = input("Enter the second person's name: ")
        age = int(input("Enter the second person's age: "))
        password = input("Enter the second person's password: ")
        email = input("Enter the second person's email: ")
        user_two = User(name, age, email, password)
        print("Thank you for registering two people. Please create your bank accounts.")

        user_one_balance = bank_creation(user_one.name)
        user_two_balance = bank_creation(user_two.name)
        user_one_bank = Bank(user_one.name, user_one.age, user_one.email, user_one_balance, user_one.password.decode())
        user_two_bank = Bank(user_two.name, user_two.age, user_two.email, user_two_balance, user_two.password.decode())
        flag = options(user_two)
        if flag == False:
            break
    else: 
        user_one_balance = bank_creation(user_one.name)
        user_one_bank = Bank(user_one.name, user_one.age, user_one.email, user_one_balance, user_one.password.decode())
        flag = options(user_two)
        if flag == False:
            break
