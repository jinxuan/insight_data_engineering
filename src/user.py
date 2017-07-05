#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide class
Author: Jinxuan Wu
"""
import logging
from utility import PriorityQueue

class User(object):
    """
    This class defines a graph node represent a user
    """
    def __init__(self, id, T, D):
        self.id = id
        self.T = T
        self.D = D
        self.networks = {} # dictionary of id:degree, where degree is less than D
        self.friends = set()
        self.purchase_list = PriorityQueue(T)

    def add_friend(self, friend):
        self.friends.add(friend)

    def delete_friend(self, id):
        self.friends.remove(id)

    def add_purchase(self, amount, timestamp):
        self.purchase_list.push((timestamp, amount))



