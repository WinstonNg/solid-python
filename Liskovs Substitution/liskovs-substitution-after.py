'''
    Liskov's Substitution Principle
    -----
    Objects of a superclass can be replaced with objects of a subclass without affecting the program's correctness
    
    Solution
    -----
    One way to solve it is to remove the dependency on security codes from the pay method
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

class PaymentProcessor(ABC):
    '''
    Create an abstract base class, which sub-classes can inherit from.
    '''

    def __init__(self, security_code):
        self.security_code = security_code

    @abstractmethod
    def pay(self, order):
        '''
        Create an abstract method, leave the implementation for sub-classes
        '''
        pass

class DebitPaymentProcesor(PaymentProcessor):
    '''
    Create a debit payment sub-class that inherits from PaymentProcessor abstract class
    to process debit payment only
    '''

    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
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

    def __init__(self, email_address):
        self.email_address = email_address

    def pay(self, order):
        print("Processing paypal payment type")
        print(f"Verifying security code: {self.email_address}")
        order.status = "paid"


order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)

print(order.total_price())
processor = PaypalPaymentProcessor("monkey@gmail.com")
processor.pay(order)