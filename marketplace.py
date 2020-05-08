"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Lock

class Marketplace(object):
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producers = [] # list holding all producer queues
        self.carts = [] # list holding all consumer carts
        self.lock = Lock() # a lock used for critical sections

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        new_producer_queue = []
        with self.lock:
            idx = len(self.producers) # the new index is the current size
            self.producers.append(new_producer_queue) # add a new empty queue

        # return id as a String 'prod<id>'
        return 'prod' + str(idx)

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        # get the index from "prod<id>" string
        idx = int(producer_id[4:])
        # get corresponding queue
        producer_queue = self.producers[idx]
        # check if capacity allows a new product
        if len(producer_queue) >= self.queue_size_per_producer:
            return False
        # add product
        self.producers[idx].append(product)

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        new_cart = []
        with self.lock:
            idx = len(self.carts) # the new index is the current size
            self.carts.append(new_cart) # add a new empty cart

        return idx

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        was_found = False

        # iterate through every producer queue
        for producer_queue in self.producers:
            # check if wanted product exists in queue
            with self.lock:
                if product in producer_queue:
                    # remember from which producer's queue it was taken
                    producer_index = self.producers.index(producer_queue)
                    # remove product from the producer's queue
                    self.producers[producer_index].remove(product)
                    was_found = True
                    break
                
        # if product was found, add it to cart
        if was_found == True:
            # pair = (product, producer's id)
            self.carts[cart_id].append((product, producer_index)) 

        # return whether product was found or not
        return was_found

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        cart = self.carts[cart_id] # get corresponding cart
        for pair in cart:
            if product == pair[0]: # found the corresponding product
                producer_id = pair[1] # get producer's queue index
                self.carts[cart_id].remove(pair) # remove the pair from cart
                # add product back to producer's queue
                self.producers[producer_id].append(product)
                break

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        cart = self.carts[cart_id] # get corresponding cart
        # form a list with the products from the cart
        # a cart has (product, producer_id) pairs
        # so the product is the first element in a pair
        product_list = [pair[0] for pair in cart]
        self.carts[cart_id] = [] # empty cart

        return product_list
