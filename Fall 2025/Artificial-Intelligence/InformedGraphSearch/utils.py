# Used by main-nogui.py and main-gui.py
#
def loadGraphData(path):
    # Read in the city data
    with open(path, "r") as f:
        line_parts = f.readline().split(",")
        n = int(line_parts[0])
        edge_count = int(line_parts[1])

        # Read the vertices
        city_locations = []
        for i in range(n):
            line_parts = f.readline().split(",")
            x = float(line_parts[0])
            y = float(line_parts[1])
            city_locations.append((x, y))

        # Read the edges
        roads = [[] for _ in range(n)]
        for i in range(edge_count):
            line_parts = f.readline().split(",")
            a = int(line_parts[0])
            b = int(line_parts[1])
            d = float(line_parts[2])
            roads[a].append((b, d))
            roads[b].append((a, d))
        # Read the start and goal
        line_parts = f.readline().split(",")
        start = int(line_parts[0])
        goal = int(line_parts[1])

    return city_locations, roads, start, goal


def loadSolutionData(filepath):
    with open(filepath, "r") as f:
        line_parts = f.readline().split(" ")
        path = []
        for part in line_parts:
            if len(part) > 0 and part.isdigit():
                path.append(int(part))
        cost = float(f.readline())
        steps = int(f.readline())
    return path, cost, steps


def isValidPath(path, edges, start_city_id, goal_city_id):
    if path[0] != start_city_id:
        print(f"Wrong start city:{path[0]}")
        return False
    if path[-1] != goal_city_id:
        print(f"Wrong goal city:{path[-1]}")
        return False
    for i in range(len(path) - 1):
        nbrs = edges[path[i]]
        found = False
        for city, distance in nbrs:
            if city == path[i + 1]:
                found = True
                break
        if not found:
            print(f"No such edge between {path[i]} and {path[i + 1]}")
            return False
    return True
