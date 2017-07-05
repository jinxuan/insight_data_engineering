import heapq
import statistics


def check_anomalous_amount(amount_to_check, history_data):
    """
    Returns if the input amount is anomalous or not.
    Args:
        amount_to_check(float): 
        history_data(list):
    Returns:
        boolean: True if amount_to_check exceeds mean(history_data) + 3 * std(history_data)
    """
    if len(history_data) < 2:
        return (False, 0, 0)
    mean = statistics.mean(history_data)
    stdev = statistics.pstdev(history_data)
    return (amount_to_check > mean + 3 * stdev, mean, stdev)


class PriorityQueue:
    """
    PriorityQueue: a heap based priorityQueue is implemented
    """

    def __init__(self, max_length):
        """
        Initialize a min-heaps with fixed length.
        Args:
            length(int): the fixed maximum length of the sorted list.
        """
        self.__max_length = max_length
        self.heap_list = []
        self.__length = 0

    def push(self, data):
        """
        Insert a new data into the min-heap. If length is larger than max_length, 
        Args:
            data(data object): the data of the new node that needs to be inserted.
        """
        if self.__length < self.__max_length:
            heapq.heappush(self.heap_list, data)
            self.__length += 1
        else:
            heapq.heappushpop(self.heap_list, data)

    def length(self):
        """
        Get the length of the list.
        Returns:
            length(int): the length of the list
        """
        return self.__length

    def min(self):
        """
        Get the minimum value of the list.
        Returns:
            minimum_data(data object): the smallest data in the list
        """
        return self.heap_list[0]

    def get(self, order="descend"):
        """
        Get a list of data in the list in descending order.
        Returns:
            return_list(list): the sorted list in descending order
        """
        if order == "descend":
            return sorted(self.heap_list, reverse=True)
        elif order == "ascend":
            return sorted(self.heap_list)
        else:
            raise NotImplementedError("sorting order {0} is not implemented.".format(order))