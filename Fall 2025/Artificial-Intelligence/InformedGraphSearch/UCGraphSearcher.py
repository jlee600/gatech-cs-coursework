from PriorityQueue import PriorityQueue
from AbstractGraphSearcher import AbstractGraphSearcher
import math
from typing import List, Set


# Implementation of Uniform-Cost Search
class UCGraphSearcher(AbstractGraphSearcher):

    # Create the data structures
    def prepare_to_search(self):
    ## Your code here
        self.bt = {}
        self.visited = set()
        self.pq = PriorityQueue()
        self.pq.push_or_decrease(0.0, self.start_city_id)
        self.final_cost = math.inf
        self.found = False

    # Return False if more steps are required
    # Return True if there is no point to more steps
    def execute_step(self) -> bool:
    ## Your code here
        if self.pq.peek_item() is None:
            return True

        cost, city = self.pq.pop()
        if city in self.visited:
            return False
        
        if city == self.goal_city_id:
            self.found = True
            self.final_cost = cost
            return True
        self.visited.add(city)

        for neighbor, action_cost in self.action_cost[city]:
            if neighbor in self.visited:
                continue
            new_cost = cost + action_cost
            if self.pq.push_or_decrease(new_cost, neighbor):
                self.bt[neighbor] = city
        
        return False
        

    # Subclasses override to return found path
    # Return empty list if there is no path
    # If path is found, return list of names (start city first, goal city last)
    def path(self) -> List[int]:
    ## Your code here
        if not self.found:
            return []
        path = [self.goal_city_id]
        while path[-1] != self.start_city_id:
            p = self.bt.get(path[-1])
            if p is None:
                return []
            path.append(p)
        path.reverse()
        return path


    def cost(self) -> float:
    ## Your code here
        return self.final_cost


    def frontier(self) -> Set[int]:
    ## Your code here
        return self.pq.items()

    def reached(self) -> Set[int]:
    ## Your code here
        return self.visited
