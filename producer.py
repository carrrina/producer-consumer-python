"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
from time import sleep

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        # get an id for a queue to publish products to
        self.id = self.marketplace.register_producer()

    def run(self):
        while True:
            for prod in self.products:
                quantity = prod[1]
                for _ in range(quantity): # add product according to quantity
                    product = prod[0]
                    prod_sleep_time = prod[2]
                    # try to publish product
                    while self.marketplace.publish(self.id, product) is False:
                        # if queue is full, wait before retrying
                        sleep(self.republish_wait_time)
                    # wait before adding another product
                    sleep(prod_sleep_time)
