'''
    Dependency Invertion Principle
    -----
    Classes should depend on abstractions, not on concrete sub-classes
'''

'''
Credit goes to ArjanCodes
Refer to original source code here https://github.com/ArjanCodes/betterpython/tree/main
'''

from abc import ABC, abstractmethod

class Order:

    def __init__(self):
        self.items = []
        self.quantities = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self) -> bool:
        pass

class SMSAuth(Authorizer):

    authorized = False

    def verify_code(self, code):
        print(f"Verifying code: {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class NotARobot(Authorizer):

    authorized = False

    def not_a_robot(self):
        print(f"You don't appear to be a robot")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class PaymentProcessor(ABC):
    '''
    Create an abstract base class, which sub-classes can inherit from.
    '''

    @abstractmethod
    def pay(self, order):
        '''
        Create an abstract method, leave the implementation for sub-classes
        '''
        pass

# # Below class is no longer needed, due to using composition
# class PaymentProcessor_SMS(PaymentProcessor):
#     '''
#     Sub-class of PaymentProcessor

#     This class was created to ensure classes only implement auth_sms if it's needed
#     '''

#     @abstractmethod
#     def auth_sms(self, code):
#         pass


class DebitPaymentProcesor(PaymentProcessor):
    '''
    Create a debit payment sub-class that inherits from PaymentProcessor abstract class
    to process debit payment only
    '''

    def __init__(self, security_code, authorizer: Authorizer):
        self.security_code = security_code
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not Authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class CreditPaymentProcesor(PaymentProcessor):
    '''
    Create a credit payment sub-class that inherits from PaymentProcessor abstract class
    to process credit payment only
    '''

    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaypalPaymentProcessor(PaymentProcessor):
    '''
    Create a paypal payment sub-class that inherits from PaymentProcessor abstract class
    to process paypal payment only
    '''

    def __init__(self, email_address, authorizer: Authorizer):
        self.authorizer = authorizer
        self.email_address = email_address

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception('Not Authorized')
        print("Processing paypal payment type")
        print(f"Verifying security code: {self.email_address}")
        order.status = "paid"

# Create order object
order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)

print(order.total_price())
authorizer = SMSAuth()
# NotARobot auth can be added, because the classes do not depend on SMSAuth concrete class, but on Authorizer abstract class
robot_authorizer = NotARobot()
processor = DebitPaymentProcesor("2345678", authorizer)
robot_authorizer.not_a_robot()
authorizer.verify_code(465839)
processor.pay(order)