import math
from collections import defaultdict
from money.money import Money
from money.currency import Currency


class ShoppingApp(object):

    # Here we have the predefined product catalogue as requirements didn't ask for any db :)
    # i did not see any purposed of having these data in some kind of structured json like data, as that can be
    # later on structured if a db is involved and data is mined out with some kind of a templating method
    product_catalogue = {"Baked Beans": 0.99, "Biscuits": 1.20, "Sardines": 1.89, "Shampoo Small": 2.00,
                         "Shampoo Medium": 2.50, "Shampoo Large": 3.50}
    # adding sardines and baked beans here, this dictionary can be extended later on
    # if new offer is going to appear - this also can be replaced with a db query
    discount_catalog = ["Basket Beans", "Sardines"]

    # maybe this is going to be a list instead of a dictionary because new offers may come in.
    # So the usage of a set would not be a good choice
    # then the usage of a set would be much more efficient from a element accessing perspective
    product_offer = ["Shampoo Small", "Shampoo Medium", "Shampoo Large"]

    def __init__(self):
        self.items_in_basket = defaultdict()
        self.total = 0
        self.sub_total = 0
        self.applied_discounts = 0

    # in case we want to extend our basket we can ad further elements into it - can be replace with db query
    def add_item_to_basket(self, product_name, product_price):
        if product_name is not None and product_name not in self.product_catalogue:
            self.product_catalogue.update({product_name: product_price})

    def populate_basket_with_items(self, item_name, item_quantity):
        # edge cases can be considered like if we are talking about a bread then we can by 1/2 for 1/2 of price
        if item_name is not None and item_quantity >= 1:
            self.items_in_basket.update({item_name: item_quantity})

    def doing_the_math(self):
        for product_name, product_quantity in self.items_in_basket.items():
            get_price = self.product_catalogue[product_name]
            # this is going to calculate the product total and later on the necessary
            # Money and Currency functions will do the roundings
            if product_quantity:
                self.sub_total += (product_quantity * get_price)

            if product_name == "Sardines" and product_quantity:
                self.applied_discounts += product_quantity*get_price*0.25

            elif product_name == "Baked Beans" and product_quantity:
                self.applied_discounts += int(product_quantity/3)*get_price

        self.total = self.rounding_function((self.sub_total - self.applied_discounts),2)
        self.sub_total = self.rounding_function(self.sub_total,2)
        self.applied_discounts = self.rounding_function(self.applied_discounts,2)


            # this was a another approach as i wanted to make a predefined catalog with the offers
            # wasn't actually a really good idea because of performance issues
            # would that been easier if theres a db so we could read data out(the offers)
            # dynamically data reading would increase perfromance of the code
            # for stuff in self.discount_catalog:
            #     if stuff == "Baked Beans":

    # maybe this could be written much more better
    # For example instead of a dictionary the overall totals could be just written out
    # as a report to make it better from a performance perspective
    def calculate_bill(self):
        self.doing_the_math()
        print(self.sub_total)
        print(self.applied_discounts)
        print(self.total)

        return {"sub_total_bill": Money(str(self.sub_total), Currency.GBP),
                "discount_applied": Money(str(self.applied_discounts), Currency.GBP),
                "total_calculated": Money(str(self.total), Currency.GBP)}

    def doing_the_math_with_new_offer(self):

        total_quantity = 0
        offer_price = 0

        for product_name, product_quantiy in self.items_in_basket.items():
            price = self.product_catalogue[product_name]
            offer_price = price if offer_price == 0 else min(price, offer_price)

            if product_quantiy:
                self.sub_total += (product_quantiy * price)

            if product_name in self.product_offer:

                if product_quantiy > 2:
                    self.applied_discounts += int(product_quantiy/3)*price
                    total_quantity += product_quantiy - int(product_quantiy/3)*product_quantiy
                else:
                    total_quantity += product_quantiy

                # here we are going to calculate the last edge case: if stuff exceeds 2
                if total_quantity > 2:
                    self.applied_discounts += int(total_quantity/3)*offer_price
                    total_quantity -= int(total_quantity/3)*total_quantity

        self.sub_total = self.rounding_function(self.sub_total, 2)
        self.applied_discounts = self.rounding_function(self.applied_discounts, 2)
        self.total = self.rounding_function(self.sub_total - self.applied_discounts, 2)


    # https://stackoverflow.com/questions/2356501/how-do-you-round-up-a-number-in-python
    @staticmethod
    def rounding_function(number, decimals=0):
        print(number)
        multiplier = 10 ** decimals
        return math.ceil(number * multiplier) / multiplier


    def calculate_bill_if_offer(self):

        self.doing_the_math_with_new_offer()
        print(self.sub_total)
        return {"sub_total_bill": Money(str(self.sub_total), Currency.GBP),
                "discount_applied": Money(str(self.applied_discounts), Currency.GBP),
                "total_calculated": Money(str(self.total), Currency.GBP)}
    # now if we want to get rid of some purchased item then we can call this function

    def lets_get_rid_of_something(self, product_name, product_quantity):

        try:
            if product_name in self.items_in_basket and product_quantity >= self.items_in_basket[product_name]:
                self.items_in_basket.pop(product_name, None)
            self.items_in_basket[product_name] -= product_quantity
        except(KeyError, RuntimeError):
            pass
        # we can write a logger here, just to log the runtime errors or when catching an error
        # in order to be able to identify issues

    def final_checkout(self, cash):

        if cash < self.sub_total:
            return "You need more money"
        balance = cash - self.sub_total

        return balance

    # this class can be moved to another module if extended but now i guess there is no need
    # to move it to another one as its too small
    # this class is intended to do the test operations


    # code removed used for debugging

# if __name__ == '__main__':
#
#     instanciate = ShoppingApp()
#
#     Basket = {"Baked Beans": 4, "Biscuits": 1}
#
#     for product_name, product_quantity in Basket.items():
#         print(product_name)
#         instanciate.populate_basket_with_items(product_name, product_quantity)
#
#     testing_bills = list(instanciate.calculate_bill().values())
#     print(type(testing_bills[0]))