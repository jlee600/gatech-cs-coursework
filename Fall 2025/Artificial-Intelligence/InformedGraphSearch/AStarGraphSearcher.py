from PriorityQueue import PriorityQueue
from AbstractGraphSearcher import AbstractGraphSearcher
import math
from typing import List, Set


# Implementation of A* Search
class AStarGraphSearcher(AbstractGraphSearcher):

    # For our heuristic
    def estimated_remaining_cost(self, city_id):
    ## Your code here
        x1, y1 = self.city_locations[city_id]
        x2, y2 = self.city_locations[self.goal_city_id]
        return math.hypot(x1 - x2, y1 - y2)

    # Create the data structures
    def prepare_to_search(self):
    ## Your code here
        self.pq = PriorityQueue()
        self.bt = {}
        est = self.estimated_remaining_cost(self.start_city_id)
        self.pq.push_or_decrease(0.0 + est, self.start_city_id)
        self.bt[self.start_city_id] = None, 0.0, 0.0
        self.final_cost = math.inf
        self.found = False

    # Return False if more steps are required
    # Return True if there is no point to more steps
    def execute_step(self) -> bool:
    ## Your code here
        if self.pq.peek_item() is None:
            self.final_cost = math.inf
            self.found = False
            return True
        _, city = self.pq.pop()
        
        if city == self.goal_city_id:
            self.final_cost = self.bt[city][2]
            self.found = True
            return True
        _, _, Rcost = self.bt[city]

        for neighbor, action_cost in self.action_cost[city]:
            new_cost = Rcost + action_cost
            est = self.estimated_remaining_cost(neighbor)
            if neighbor not in self.bt or new_cost < self.bt[neighbor][2]:
                self.pq.push_or_decrease(new_cost + est, neighbor)
                self.bt[neighbor] = city, action_cost, new_cost

        return False

    # Subclasses override to return found path
    # Return empty list if there is no path
    # If path is found, return list of names (start city first, goal city last)
    def path(self) -> List[int]:
    ## Your code here
        if not self.found:
            return []
        # if self.goal_city_id not in self.bt:
        #     return []
        path = []
        city = self.goal_city_id
        while city is not None:
            path.append(city)
            city = self.bt[city][0]
        path.reverse()
        return path

    def cost(self) -> float:
    ## Your code here
        if self.goal_city_id not in self.bt:
            return math.inf
        return self.final_cost

    def frontier(self) -> Set[int]:
    ## Your code here
        return self.pq.items()

    def reached(self) -> Set[int]:
    ## Your code here
        return self.bt.keys()
