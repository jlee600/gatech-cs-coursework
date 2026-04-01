import math
from typing import List, Set


# Each algorithm implemented will be a subclass of AbstractMapSearcher
class AbstractGraphSearcher:

    # Store the problem in instance variables
    def __init__(self, city_locations, action_cost, start_city_id, goal_city_id):
        self.city_locations = city_locations
        self.action_cost = action_cost
        self.start_city_id = start_city_id
        self.goal_city_id = goal_city_id

    # Subclasses override to set up any data structures you need
    def prepare_to_solve(self):
        pass

    # Subclasses override to do one step
    # Return False if more steps are required
    # Return True if there is no point to more steps
    def execute_step(self) -> bool:
        return True

    # Subclasses override to return found path
    # Return empty list if there is no path
    # If path is found, return list of names (start city first, goal city last)
    def path(self) -> List[int]:
        return []

    # Returns the cost of the path
    # No path? math.inf
    def cost(self) -> float:
        return math.inf

    # Cities in the search queue
    def frontier(self) -> Set[int]:
        return set()

    # Cities that have been reached
    # You know how to get from the initial state to these
    # cities (or, for bidirectional, how to get to the goal from these)
    def reached(self) -> Set[int]:
        return set()
