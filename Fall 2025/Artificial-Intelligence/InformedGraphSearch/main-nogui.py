import sys
from time import perf_counter
import os
import utils

# Usage:
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <graph> <searcher>")
    exit(-1)

# Read command-line args
cities_file = sys.argv[1]
search_classname = sys.argv[2]

# Read in the city data
city_locations, action_cost, start_city_id, goal_city_id = utils.loadGraphData(
    cities_file
)
city_count = len(city_locations)

# Print facts
print(f"{city_count:,d} Cities: start={start_city_id}, goal={goal_city_id}")

# We can accept the name of the class or the name of the file
search_classname = search_classname.removesuffix(".py")

# Create Map Searcher (assumes module and class have same name)
print(f"Searcher: {search_classname}")
search_module = module = __import__(search_classname)
search_class = getattr(search_module, search_classname)
map_searcher = search_class(city_locations, action_cost, start_city_id, goal_city_id)

# Let's time the search
start_time = perf_counter()

map_searcher.prepare_to_search()

is_done = False
step_count = 0
while not is_done:
    is_done = map_searcher.execute_step()
    step_count += 1

stop_time = perf_counter()
# Show some stats
print(f"Search time: {1000.0 * (stop_time - start_time):.2f} ms.")
print(f"Steps:{step_count:,d}")

# Show the result
path = map_searcher.path()
# print(f"Path: {path}")
if not utils.isValidPath(path, action_cost, start_city_id, goal_city_id):
    print("*** Error: Path is invalid. ***")

cost = map_searcher.cost()
print(f"Cost: {cost:,.2f}")
print(f"Path length: {len(path)}")

# Check it against the solution file if one exists
prob_dir = os.path.dirname(cities_file)
solution_path = os.path.join(prob_dir, f"path-{search_classname}-{city_count}.txt")
if os.path.exists(solution_path):
    true_path, true_cost, true_steps = utils.loadSolutionData(solution_path)

    # It should be within 0.01 of the solution
    if true_cost + 0.01 < cost:
        print(
            f"*** Error: Your solution is non-optimal. Yours:{cost:.4f} Solution:{true_cost:.4f} ***"
        )

    # Print an error if the step count is off by more than 10 percent
    if abs(true_steps - step_count) / true_steps > 0.1:
        print(
            f"*** Error: Wrong number of iterations. Yours:{step_count:,d} Solution:{true_steps:,d} ***"
        )

# For generating the solution files
# with open(solution_path, "w") as f:
#     for p in path:
#         print(f"{p} ", end="", file=f)
#     print("", file=f)
#     print(f"{cost:.3f}", file=f)
#     print(f"{count}", file=f)
