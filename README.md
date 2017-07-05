# Assumption
Number of Purchase Even >> Friend Event > Un Friend Event

# Environment
Python 3.5

# Implementation Details
The data structure I used to solve this problem is a undirected graph, where each node contains a <key, value> dictionary where key is the neighbor id and value is the shortest distance to the neighbor. Each node also contains a list of tuples represent purchase history<amount, timestamp>.  

# Usage
```
pip install tqdm
sh ./run.sh`
```


# Complexity Analysis

For purchase event, time complexity is O(n), where n is the number of friends in the degree d network. I traverse a local 
For add friend event, time complexity is O(n), 
For unfriend  event, time complexity is O(n^2), for all the impacted node in the network, we need to use BFS to recalculate its neighbors's degree.

# Discussion

# Sample Data Distribution

| Event Name        | Count           |
| ------------- |:-------------:|
| purchase      | 401036 |
| befriend      | 94980      |
| unfriend | 4983      |

## Space-Time trade off
There are several design with different space-time trade off. Specifically, they are
1. For each user node, only store its degree 1 friend and its own purchase history. 
    1. For each purchase event, need to do a BFS.
    2. For each addfriend event, need to do a BFS.
    3. For each delete friend event, need to do a BFS.
    
2. For each user node, store its degree D friends list and its own purchase history. 
    1. For each purchase event, traverse a friend list. only append to its own purchase history.
    2. For each addfriend event, traverse local friend list.
    3. For each delete friend event, need to do N BFS.
    
3. For each user node, store its degree D friends list and its network purchase history.
    
    1. For each purchase event, traverse a friend list. Append to its network purchase history.
    2. Assume use same implementation in 2 for friend event. 
    
    #### Theory Space-Time trade off comparison
    
| Implementation        | Space           | Time  |
| ------------- |:-------------:| -----:|
| 1    | Low | Slow |
| 2     | Medium     |   Medium |
| 3 | Large      |    Fast |



## Scalability
Based on the space-time trade off discussed above, I choose the second programming model largely for scalability. The most easy to implement approach is the first model mentioned above. But when data is large enough, we have to shard or partition data to different compute node. Doing BFS frequently through network IO is a bad idea and will cost a lot of time.

By saving degree d netork locally in each graph node, once the batch processing mode is finished the network will be relative stable. So the network IO mentioned above could be saved quite a bit. 
 
## Streaming Error Handling
In real world streaming data could arrive out of order or comes from different data source. Specifically, if an unfriend event comes after purchase event. The file output could be wrong. 
In current version of code I don't write out until we process all input streamming data. So one way to solve this problem whenever a unfriend event arrived. We need to go back and check if this will impact the judgement of anomaly activity. 

## Streaming windowing
There could exists situtaion where among the T most recent history, the time window is too large like couple of month. We could add an additional option to filter out data that is too old by a user defined threshold when calling anomaly detection function.
 
## High D value
Based on the famous six degrees of separation,  all living things and everything else in the world are six or fewer steps away from each other. This implies if that if the input D  is large. My programming model will consume too much memory.  