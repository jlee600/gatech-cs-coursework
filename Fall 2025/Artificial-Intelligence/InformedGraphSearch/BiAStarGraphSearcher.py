from PriorityQueue import PriorityQueue
from AbstractGraphSearcher import AbstractGraphSearcher
import math
from typing import List, Set


# Implementation of Bidirecitonal A* Search
class BiAStarGraphSearcher(AbstractGraphSearcher):

    # For our heuristic
    def estimated_remaining_cost(self, city_id):
    ## Your code here
        x1, y1 = self.city_locations[city_id]
        x2, y2 = self.city_locations[self.goal_city_id]
        return math.hypot(x1 - x2, y1 - y2)
    
    def estimated_remaining_cost_backward(self, city_id):
        x1, y1 = self.city_locations[city_id]
        x2, y2 = self.city_locations[self.start_city_id]
        return math.hypot(x1 - x2, y1 - y2)

    # Create the data structures
    def prepare_to_search(self):
    ## Your code here
        self.fbt = {}
        self.bbt = {}
        self.forwardQ = PriorityQueue()
        self.backwardQ = PriorityQueue()
        
        forward_est = self.estimated_remaining_cost(self.start_city_id)
        self.forwardQ.push_or_decrease(0.0 + forward_est, self.start_city_id)
        self.fbt[self.start_city_id] = None, 0.0 # prev, cost

        backward_est = self.estimated_remaining_cost_backward(self.goal_city_id)
        self.backwardQ.push_or_decrease(0.0 + backward_est, self.goal_city_id)
        self.bbt[self.goal_city_id] = None, 0.0

        self.final_cost = math.inf 
        self.bridge = None
        
    # Return False if more steps are required
    # Return True if there is no point to more steps
    def execute_step(self) -> bool:
    ## Your code here
        if len(self.forwardQ) == 0 or len(self.backwardQ) == 0:
            return True

        Rf = self.forwardQ.peek_priority()
        Rb = self.backwardQ.peek_priority()

        if self.final_cost < math.inf and Rf >= self.final_cost and Rb >= self.final_cost:
            return True

        if Rf <= Rb: # forward
            _, city = self.forwardQ.pop()
            prev, Rcost = self.fbt[city]

            # if city in self.bbt:
            #     total = Rcost + self.bbt[city][1]
            #     if total < self.final_cost:
            #         self.final_cost = total
            #         self.bridge = city, city

            for neighbor, action_cost in self.action_cost[city]:
                temp = Rcost + action_cost

                if neighbor in self.bbt:
                    total_cost = temp + self.bbt[neighbor][1]
                    if total_cost < self.final_cost:
                        self.final_cost = total_cost
                        self.bridge = city, neighbor

                old = self.fbt.get(neighbor)
                if old is None or temp < old[1]:
                    best = math.inf
                    for x in self.backwardQ.items():
                        bx = self.bbt.get(x)
                        if bx is None:
                            continue
                        
                        x1, y1 = self.city_locations[neighbor]
                        x2, y2 = self.city_locations[x]
                        cand = math.hypot(x1 - x2, y1 - y2) + bx[1] 
                        best = min(best, cand)
                
                    if best == math.inf:
                        best = self.estimated_remaining_cost(neighbor) 
                    
                    f = temp + best
                    self.fbt[neighbor] = city, temp
                    self.forwardQ.push_or_decrease(f, neighbor)

        else:  # backward
            _, city = self.backwardQ.pop()
            prev, Rcost = self.bbt[city]

            # if city in self.fbt:
            #     total = Rcost + self.fbt[city][1]
            #     if total < self.final_cost:
            #         self.final_cost = total
            #         self.bridge = city, city

            for neighbor, action_cost in self.action_cost[city]:
                temp = Rcost + action_cost

                if neighbor in self.fbt:
                    total_cost = temp + self.fbt[neighbor][1]
                    if total_cost < self.final_cost:
                        self.final_cost = total_cost
                        self.bridge = neighbor, city

                old = self.bbt.get(neighbor)
                if old is None or temp < old[1]:
                    best = math.inf
                    for x in self.forwardQ.items():
                        fx = self.fbt.get(x)
                        if fx is None:
                            continue
                        
                        x1, y1 = self.city_locations[neighbor]
                        x2, y2 = self.city_locations[x]
                        cand = math.hypot(x1 - x2, y1 - y2) + fx[1]  
                        best = min(best, cand)

                    if best == math.inf:
                        best = self.estimated_remaining_cost_backward(neighbor)

                    f = temp + best
                    self.bbt[neighbor] = city, temp
                    self.backwardQ.push_or_decrease(f, neighbor)

        return False
            
    # Subclasses override to return found path
    # Return empty list if there is no path
    # If path is found, return list of names (start city first, goal city last)
    def path(self) -> List[int]:
    ## Your code here
        if self.bridge is None or self.final_cost == math.inf:
            return []
        
        left = []
        s = self.bridge[0]
        while s is not None:
            left.append(s)
            s = self.fbt[s][0]
        left.reverse()
        
        right = []
        s = self.bridge[1]
        while s is not None:
            right.append(s)
            s = self.bbt[s][0]
        
        if left is not None and right is not None and left[-1] == right[0]:
            right = right[1:]
        return left + right


    def cost(self) -> float:
    ## Your code here
        if self.bridge is None:
            return math.inf
        return self.final_cost

    def frontier(self) -> Set[int]:
    ## Your code here
        return self.forwardQ.items().union(self.backwardQ.items())

    def reached(self) -> Set[int]:
    ## Your code here
        return set(self.fbt.keys()).union(set(self.bbt.keys()))

