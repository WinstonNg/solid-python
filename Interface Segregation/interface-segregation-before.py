'''
    Interface Segregation Principle
    -----
    No code should be forced to depend on methods it does not use
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

    # auth_sms is not used by CreditPaymentProcessor
    # This forces subclasses to implement (or raise an exception for) functionality they don’t use, which is a violation of ISP
    @abstractmethod
    def auth_sms(self, code):
        pass

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
        self.is_verified = False

    def auth_sms(self, code):
        print(f'Verifying sms code: {code}')
        self.is_verified = True

    def pay(self, order):
        if not self.is_verified:
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

    # auth_sms is not used by CreditPaymentProcesor, this usage violates Interface Segregation Principle
    # auth_sms in CreditPaymentProcessor also violates Liskov's substitution principle
    def auth_sms(self, code):
        raise Exception("Credit card payment don't support SMS code authorization")

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
        self.is_verified = False

    def auth_sms(self, code):
        print(f'Verifying sms code: {code}')
        self.is_verified = True

    def pay(self, order):
        if not self.is_verified:
            raise Exception('Not Authorized')
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