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

            if product_name =="Sardines" and product_quantity:
                self.
            #
            # for stuff in self.discount_catalog:
            #     if stuff == "Baked Beans":



        pass


    def calculate_bill(self):
        pass



