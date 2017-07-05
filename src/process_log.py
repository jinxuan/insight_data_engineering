#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Main program. Read in a log file of social network events and output anomality events. 
Author: Jinxuan Wu
"""
import json
from pathlib import Path

from datetime import datetime
from utility import check_anomalous_amount
from social_graph import SocialGraph
from tqdm import tqdm

#Main program


class ProcessLog(object):
    # Init build graph from input file
    def batch_process(self):
        batch_log_input = "log_input/batch_log.json"
        with open(batch_log_input, buffering=(2<<16) + 8) as f:
            line = f.readline()
            d = json.loads(line)
            T = d['T']
            D = d['D']
            self.social_graph = SocialGraph(T, D)
            for line in tqdm(f):
                # Create Social Graph
                d = json.loads(line)
                event_type = d["event_type"]
                if event_type == "purchase":
                    self.social_graph.add_purchase(d["id"], d["amount"], d["timestamp"])
                elif event_type == "befriend":
                    self.social_graph.add_friend(d["id1"], d["id2"])
                elif event_type == "unfriend":
                    self.social_graph.delete_friend(d["id1"], d["id2"])
        flagged_purchase_output_file = 'log_output/flagged_purchases.json'
        Path(flagged_purchase_output_file).touch()
        with open(flagged_purchase_output_file, "w") as f:
            f.write('\n'.join(self.social_graph.anomaly_records))

    #Feature 1
    def stream_process(self):
        batch_log_input = "log_input/stream_log.json"
        with open(batch_log_input) as f:
            for line in tqdm(f):
                # Create Social Graph
                d = json.loads(line)
                event_type = d["event_type"]

                if event_type == "purchase":
                    self.social_graph.add_purchase(d["id"], d["amount"], d["timestamp"])
                elif event_type == "befriend":
                    self.social_graph.add_friend(d["id1"], d["id2"])
                elif event_type == "unfriend":
                    self.social_graph.delete_friend(d["id1"], d["id2"])
            flagged_purchase_output_file = 'log_output/flagged_purchases.json'
            Path(flagged_purchase_output_file).touch()
            with open(flagged_purchase_output_file, "w") as f:
                for line in self.social_graph.anomaly_records:
                    f.write(line + '\n')
        flagged_purchase_output_file = 'log_output/flagged_purchases.json'
        Path(flagged_purchase_output_file).touch()
        with open(flagged_purchase_output_file, "w") as f:
            f.write('\n'.join(self.social_graph.anomaly_records))


if __name__ == '__main__':
    process_log = ProcessLog()
    process_log.batch_process()
    process_log.stream_process()
