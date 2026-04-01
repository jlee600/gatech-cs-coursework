import pickle
from tkinter import *
import sys
from importlib import import_module
import math

# Canvas size
MAX_X = 1024.0
MAX_Y = 768.0

# Usage:
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <json>")
    exit(-1)

# Read commnd-line args
assignments_file = sys.argv[1]

# Read in the data
with open(assignments_file, "rb") as infile:
    assignments = pickle.load(infile)


# How long is one edge of the hexagon
SIDE = MAX_X / (2.8 * math.sqrt(len(assignments)))

# How far from the center to the midpoint of a side?
RADIUS = math.sin(math.pi / 3.0) * SIDE

# Inset to first center
INSET_X = SIDE * 1.1
INSET_Y = SIDE * 1.1
# Set up a resizable window with a canvas
top = Tk()
top.resizable(True, True)
canvas = Canvas(top, bg="white", height=MAX_Y, width=MAX_X)
top.bind("<Configure>", lambda e: on_resize(e, canvas))


color_dict = {
    "high": "orange",
    "low": "yellow",
    "artillery": "red",
    "dining": "lightblue",
}

def on_resize(event, canvas):
    if event.widget is not canvas.master:
        return
    W, H = canvas.winfo_width(), canvas.winfo_height()
    if W <= 2 or H <= 2:
        return
    bbox = canvas.bbox("all")
    if not bbox:
        return
    x0, y0, x1, y1 = bbox
    bw, bh = max(1, x1 - x0), max(1, y1 - y0)
    margin = 10
    scale = min((W - 2 * margin) / bw, (H - 2 * margin) / bh)
    if scale <= 0:
        return
    last = getattr(canvas, "_last_fit_scale", None)
    if last:
        inv = 1.0 / last
        canvas.scale("all", 0, 0, inv, inv)
    canvas.scale("all", 0, 0, scale, scale)
    canvas._last_fit_scale = scale
    x0, y0, x1, y1 = canvas.bbox("all")
    bw, bh = x1 - x0, y1 - y0
    dx = (W - bw) / 2 - x0
    dy = (H - bh) / 2 - y0
    canvas.move("all", dx, dy)
    
def _hex_neighbors(row, col):
    """
    Neighbors for the 'doubled-rows, column-offset' hex coords:
      - rows advance by ±2 for vertical neighbors in the same column
      - crossing to col±1 uses row±1
    Returns the 6 edge neighbors
    """
    return [
        (row - 2, col),
        (row + 2, col),
        (row - 1, col - 1),
        (row + 1, col - 1),
        (row - 1, col + 1),
        (row + 1, col + 1),
    ]
    
def evaluate(assignments):
    """
    assignments: dict keyed by (row, col) -> (use_type, people_count)
    Prints:
      - Version A adjacency check (artillery-artillery)
      - Version B people limit
      - Version B no artillery-high adjacency
      - Final Version high must neighbor dining
      - Totals: people and artillery count
    Returns (ok, total_people)
    """

    storage = set()
    high = set()
    dining = set()
    total_people = 0

    for (r, c), (use_type, people_count) in assignments.items():
        total_people += int(people_count)
        t = str(use_type).lower()
        if t == "artillery":
            storage.add((r, c))
        elif t == "high":
            high.add((r, c))
        elif t == "dining":
            dining.add((r, c))
        if t in ("artillery", "high", "dining"):
            print(f"DEBUG: ({r},{c}) -> raw='{use_type}', normalized='{t}'")

    # Version A: no artillery cells adjacent
    va_ok = True
    for (r, c) in storage:
        for (nr, nc) in _hex_neighbors(r, c):
            if (nr, nc) in storage:
                va_ok = False
                break
        if not va_ok:
            break

    # Version B: people limit
    vb_people_limit_ok = (total_people <= len(storage) * 1200)

    # Version B: artillery and high may not share an edge
    vb_no_artillery_high_adj_ok = True
    for (r, c) in storage:
        for (nr, nc) in _hex_neighbors(r, c):
            if (nr, nc) in high:
                vb_no_artillery_high_adj_ok = False
                break
        if not vb_no_artillery_high_adj_ok:
            break

    # Final Version: every high must be adjacent to at least one dining
    final_ok = True
    for (r, c) in high:
        print(f"DEBUG: High cell at ({r},{c}) has neighbors {[ (nr,nc) for (nr,nc) in _hex_neighbors(r,c) ]}")
        print(f"DEBUG: Dining cells are {list(dining)}")
        if not any((nr, nc) in dining for (nr, nc) in _hex_neighbors(r, c)):
            final_ok = False
            break
    print(f"Version A: No artillery storage cells can be adjacent to each other: {'Correct' if va_ok else 'Incorrect'}")
    print(f"Version B: The total number of people in the camp cannot be greater than the number of artillery storage cells times 1,200: {'Correct' if vb_people_limit_ok else 'Incorrect'}")
    print(f"Version B: Artillery storage cells and high-density housing may not share an edge: {'Correct' if vb_no_artillery_high_adj_ok else 'Incorrect'}")
    print(f"Final Version: Every high-density housing cell must be adjacent to at least one dining services cell: {'Correct' if final_ok else 'Incorrect'}")
    print(f"You have {total_people} people, {len(storage)} artillery storage cells, and {len(dining)} dining cells")

    ok = va_ok and vb_people_limit_ok and vb_no_artillery_high_adj_ok and final_ok
    return ok, total_people


def make_hexagon(canvas, center_x, center_y, use_type, people_count):
    color = color_dict[use_type]
    if use_type in ["low", "high"]:
        label = f"{use_type}: {people_count}"
    else:
        label = use_type

    canvas.create_polygon(
        center_x - SIDE,
        center_y,
        center_x - SIDE / 2.0,
        center_y - RADIUS,
        center_x + SIDE / 2.0,
        center_y - RADIUS,
        center_x + SIDE,
        center_y,
        center_x + SIDE / 2.0,
        center_y + RADIUS,
        center_x - SIDE / 2.0,
        center_y + RADIUS,
        fill=color,
        outline="black",
    )
    canvas.create_text(center_x, center_y, text=label)


for ((row, col), (use_type, people_count)) in assignments.items():

    # Find the center
    x = INSET_X + 1.5 * SIDE * col
    y = INSET_Y + RADIUS * row

    # Pick a color
    make_hexagon(canvas, x, y, use_type, people_count)
    
# Evaluate and print the required summary
_ = evaluate(assignments)

# Render it!
canvas.pack(fill=BOTH, expand=True)

# Start the event loop
top.mainloop()
