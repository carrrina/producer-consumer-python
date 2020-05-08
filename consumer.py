"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from __future__ import print_function
from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        # get a customer cart id
        cart_id = self.marketplace.new_cart()
        for cart in self.carts:
            for op in cart:
                # repeat operation according to quantity
                for _ in range(op["quantity"]):
                    if op["type"] == "add":
                        while self.marketplace.add_to_cart(cart_id, op["product"]) is False:
                            sleep(self.retry_wait_time)
                    elif op["type"] == "remove":
                        self.marketplace.remove_from_cart(cart_id, op["product"])
            # place the order and empty cart
            final_products = self.marketplace.place_order(cart_id)

            # print the products ordered
            # cart_id + 1 is necessary because ids start from 0
            for prod in final_products:
                print('cons' + str(cart_id + 1) + ' bought ' + str(prod))
                