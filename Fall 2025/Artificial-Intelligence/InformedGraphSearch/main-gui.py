import json
from tkinter import *
import sys
from importlib import import_module
import math
import utils

# Canvas size
MAX_X = 1024.0
MAX_Y = 768.0

# Recoloring the roads takes time
RECOLOR_ROADS = False

# Usage:
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <graph> <searcher>")
    exit(-1)

# Read commnd-line args
cities_file = sys.argv[1]
search_classname = sys.argv[2]

city_locations, action_cost, start_city_id, goal_city_id = utils.loadGraphData(
    cities_file
)
city_count = len(city_locations)

# How big are the city rectangles?
RECT_RADIUS = 3 + 20 / math.sqrt(len(city_locations))

# How big is the box around the end points?
END_RADIUS = 1.5 * RECT_RADIUS + 2.0

# How much delay between screen updates
delay = int(1000 / math.sqrt(city_count))  # ms

# We can accept the name of the class or the name of the file
search_classname = search_classname.removesuffix(".py")

# Create Map Searcher (assumes module and class have same name)
print(f"Searcher: {search_classname}")
search_module = __import__(search_classname)
search_class = getattr(search_module, search_classname)
map_searcher = search_class(city_locations, action_cost, start_city_id, goal_city_id)
map_searcher.prepare_to_search()

# Set up a non-resizable window with a canvas
top = Tk()
canvas = Canvas(top, bg="white", height=MAX_Y, width=MAX_X)
top.resizable(False, False)

# Highlight the start and goal cities
coords_start = city_locations[start_city_id]
canvas.create_rectangle(
    coords_start[0] - END_RADIUS,
    coords_start[1] - END_RADIUS,
    coords_start[0] + END_RADIUS,
    coords_start[1] + END_RADIUS,
    fill="orange",
)
coords_goal = city_locations[goal_city_id]
canvas.create_rectangle(
    coords_goal[0] - END_RADIUS,
    coords_goal[1] - END_RADIUS,
    coords_goal[0] + END_RADIUS,
    coords_goal[1] + END_RADIUS,
    fill="lightgreen",
)

# An empty path means one has not been found
path = []

##  Make the rendering objects for all cities and edges (in black)
## (We will not create any more objects -- just edit these and re-pack)

# Make the road lines
edge_dict = {}
for a_city_index in range(len(city_locations)):
    connection_list = action_cost[a_city_index]
    for b_city_index, _ in connection_list:
        if b_city_index < a_city_index:
            continue

        coords_a = city_locations[a_city_index]
        coords_b = city_locations[b_city_index]

        edge = canvas.create_line(
            coords_a[0], coords_a[1], coords_b[0], coords_b[1], fill="lightgrey"
        )
        edge_dict[(a_city_index, b_city_index)] = edge

# Make the city rects
city_rects = []
for city in city_locations:
    x = city[0]
    y = city[1]
    rect = canvas.create_rectangle(
        x - RECT_RADIUS, y - RECT_RADIUS, x + RECT_RADIUS, y + RECT_RADIUS, fill="black"
    )
    city_rects.append(rect)

# Render it!
canvas.pack()


def colorpath(apath, acolor):
    global canvas, edge_dict
    for i in range(len(apath) - 1):
        city_a = apath[i]
        city_b = apath[i + 1]
        if city_b < city_a:
            temp = city_a
            city_a = city_b
            city_b = temp
        line = edge_dict[(city_a, city_b)]
        canvas.itemconfig(line, fill=acolor)


# Will get called repeatedly until execute_step returns True
def do_step():
    global map_searcher, top, canvas, city_rects, edge_dict, path

    # Do a step
    is_done = map_searcher.execute_step()

    # What's the new situation?
    frontier = map_searcher.frontier()
    reached = map_searcher.reached()

    # Color cities accordingly
    for i in range(len(city_rects)):
        city_rect = city_rects[i]
        if i in frontier:
            canvas.itemconfig(city_rect, fill="yellow")
        elif i in reached:
            canvas.itemconfig(city_rect, fill="green")
        else:
            canvas.itemconfig(city_rect, fill="grey")

    oldpath = path
    path = map_searcher.path()
    if len(path) > 0 and path != oldpath:
        colorpath(oldpath, "lightgrey")
        colorpath(path, "red")

    # Do we need to schedule another run?
    if not is_done:
        top.after(delay, do_step)
    else:
        # Or show the result
        print(f"Path: {path}")

        # Color the cities red
        for city in path:
            city_rect = city_rects[city]
            canvas.itemconfig(city_rect, fill="red")

        cost = map_searcher.cost()
        print(f"Cost: {cost:,.2f}")

    # Redraw
    canvas.pack()


# Let's go!
top.after(1000, do_step)
top.mainloop()
