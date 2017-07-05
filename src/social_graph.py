#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide the class to handle all social graph related operation.  
Author: Jinxuan Wu
"""

import json
from collections import OrderedDict

from datetime import datetime
from user import User
from utility import PriorityQueue, check_anomalous_amount


class SocialGraph(object):
    """
    This class maintains information of the social graph.
    """
    def __init__(self, T, D):
        """
        :param T(str): means Last T purchases
        :param D(str): Maximum degree in graph to represent   
        """
        self.T = int(T)
        self.D = int(D)
        # Describe the graph as a python dictionary , key is user id, value is object user
        self.social_graph = {}
        # List of detected anomaly records
        self.anomaly_records = []

    def get_user(self, id):
        """
        Return the user object usde provided id.
        :param id: 
        :return: None
        """
        return self.social_graph[id]

    def add_friend(self, id1, id2):
        """
        Update all friends of user 1 and user2 with the new relationship just build.
        :param id1: user 1 id
        :param id2: user 2 id
        :return: 
        """
        if id1 not in self.social_graph:
            self.social_graph[id1] = User(id1, self.T, self.D)
        if id2 not in self.social_graph:
            self.social_graph[id2] = User(id2, self.T, self.D)
        user1 = self.social_graph[id1]
        user2 = self.social_graph[id2]
        user1.networks[user2.id] = 1
        user2.networks[user1.id] = 1

        #For each friend in user1 netowkr, add friend in user 2 network that either doesn't exist or have a lower degree now
        for user_1_friend_id, d1 in user1.networks.items():
            if d1 > self.D - 1 or user_1_friend_id == id2:
                continue
            user_1_friend = self.social_graph[user_1_friend_id]
            if user2.id not in user_1_friend.networks:
                user_1_friend.networks[user2.id] = d1 + 1
            if user2.id in user_1_friend.networks and user_1_friend.networks[user2.id] > d1 + 1:
                user_1_friend.networks[user2.id] = d1 + 1
            for uid2, d2 in user2.networks.items():
                if d1 + 1 + d2 > self.D:
                    continue
                if uid2 not in user_1_friend.networks:
                    user_1_friend.networks[uid2] = d1 + 1 + d2

        for user_2_friend_id, d1 in user2.networks.items():
            if d1 > self.D - 1 or user_2_friend_id == user1.id:
                continue
            user_2_friend = self.social_graph[user_2_friend_id]
            if user1.id not in user_2_friend.networks:
                user_2_friend.networks[user1.id] = d1 + 1
            if user1.id in user_2_friend.networks and user_2_friend.networks[user1.id] > d1 + 1:
                user_2_friend.networks[user1.id] = d1 + 1
            for uid2, d2 in user1.networks.items():
                if d1 + 1 + d2 > self.D:
                    continue
                if uid2 not in user_2_friend.networks:
                    user_2_friend.networks[uid2] = d1 + 1 + d2
        # friends means directed conntected node. Or degree 1 path.
        user1.friends.add(id2)
        user2.friends.add(id1)

    def delete_friend(self, id1, id2):
        """
        To delete a friend relationship. We need to update all friends in both user1 and user2. Use BFS here
        :param id1: 
        :param id2: 
        :return: None
        """
        user1 = self.social_graph[id1]
        user2 = self.social_graph[id2]
        user1_networks = user1.networks
        user2_networks = user2.networks
        impacted_set = set(user1_networks.keys()) | set(user2_networks.keys())
        user1.friends.remove(id2)
        user2.friends.remove(id1)
        for uid in impacted_set:
            visited = set()
            cur_level = set([uid])
            cur_user = self.social_graph[uid]
            cur_user.networks = {}
            degree = 0
            while degree <= self.D:
                next_level = set()
                for friend_id in cur_level:
                    if friend_id not in visited:
                        if degree > 0:
                            cur_user.networks[friend_id] = degree
                        visited.add(friend_id)
                        for friend_friend_id in self.social_graph[friend_id].friends:
                            if friend_friend_id not in visited:
                                next_level.add(friend_friend_id)
                cur_level = next_level
                degree += 1


    def add_purchase(self, id, amount, timestamp_str):
        """
        Add a purchase record to user's purchase history and do anomaly detection
        :param id: 
        :param amount: 
        :param timestamp_str: 
        :return: None
        """
        if id not in self.social_graph:
            self.social_graph[id] = User(id, self.T, self.D)
        self.anomaly_detection(id, amount, timestamp_str)
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        self.social_graph[id].add_purchase(amount, timestamp)

    def anomaly_detection(self, id, amount, timestamp):
        """
        Based on provided user's networks's purchase history, if the purchase is anomaly. Add anomaly record as json string to anomaly_records list
        :param id: 
        :param amount: 
        :param timestamp: 
        :return: None
        """
        network_purchase = PriorityQueue(self.T)
        user = self.social_graph[id]
        for friend_id in user.networks:
            for purchase in self.social_graph[friend_id].purchase_list.heap_list:
                network_purchase.push(purchase)
        network_purchase = list(map(lambda x:float(x[1]), network_purchase.get()))
        is_anomaly, mean, stdev = check_anomalous_amount(float(amount), network_purchase)
        if is_anomaly:
            self.anomaly_records.append(json.dumps(OrderedDict([("event_type", "purchase"),
                                                     ("timestamp",timestamp),
                                                     ("id", id),
                                                     ("amount", str(amount)),
                                                     ("mean", "{0:.2f}".format(mean)),
                                                     ("sd", "{0:.2f}".format(stdev))]), separators=(', ', ':'), ))
