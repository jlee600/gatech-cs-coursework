from ortools.sat.python import cp_model

# Constants
LOW_DENSITY = 125  # How many people will be in a low-density housing cell
HIGH_DENSITY = 500  # Max people can be in a high-density housing cell
PEOPLE_PER_STORE = 1200  # Max ratio between total people and total artillery stores

# Returns a list of tuples representing shared edges between cells
def all_neighbor_pairs(row_count, col_count):
    max_col = col_count - 1
    max_row = row_count * 2 - 1
    result = []

    # Walk the columns
    for col in range(col_count):
        offset = col % 2

        # Walk the rows
        for i in range(row_count):

            # Calculate the row index
            row = 2 * i + offset
            current_cell = (row, col)

            # Is there a neighbor to the northeast?
            if row > 0 and col < max_col:
                cell_ne = (row - 1, col + 1)
                result.append((current_cell, cell_ne))

            # Is there a neighbor to the southeast?
            if row < max_row and col < max_col:
                cell_se = (row + 1, col + 1)
                result.append((current_cell, cell_se))

            # Is there a neighbor to the direct south?
            if row < max_row - 1:
                cell_s = (row + 2, col)
                result.append((current_cell, cell_s))

    return result


# Returns a dictionary: (row, column) -> (purpose, people_count) for every cell
#    - purpose is a string: "low", "high", "artillery", or "dining"
#    - people_count is an integer representing the number of people living in the cell
#          people_count will be zero for "artillery" and "dining"
# Returns None if you could find no feasible solution

def assign_purpose(row_count, col_count):

    # Make a mopdel
    model = cp_model.CpModel()

    # Your code to describe variables, constraints, and objective function here
    cells = [(r, c) for c in range(col_count) for r in range(row_count * 2) if (r % 2) == (c % 2)]
    is_artillery_storage = {cell: model.NewBoolVar(f"artillery_{cell[0]}_{cell[1]}") for cell in cells}
    is_high = {cell: model.NewBoolVar(f"is_high_{cell[0]}_{cell[1]}") for cell in cells}
    people = {cell: model.NewIntVar(0, HIGH_DENSITY, f"people_{cell[0]}_{cell[1]}") for cell in cells}

    for cell in cells:
        model.Add(is_artillery_storage[cell] + is_high[cell] <= 1)
        model.Add(people[cell] == 0).OnlyEnforceIf(is_artillery_storage[cell])
        model.Add(people[cell] >= 126).OnlyEnforceIf(is_high[cell])
        model.Add(people[cell] <= HIGH_DENSITY).OnlyEnforceIf(is_high[cell])

        is_low = model.NewBoolVar(f"is_low_{cell[0]}_{cell[1]}")
        model.Add(is_low == 1).OnlyEnforceIf([is_artillery_storage[cell].Not(), is_high[cell].Not()])
        model.Add(is_low == 0).OnlyEnforceIf(is_artillery_storage[cell])
        model.Add(is_low == 0).OnlyEnforceIf(is_high[cell])
        model.Add(people[cell] == LOW_DENSITY).OnlyEnforceIf(is_low)

    neighbor_pairs = all_neighbor_pairs(row_count, col_count)
    for (cell1, cell2) in neighbor_pairs:
        model.Add(is_artillery_storage[cell1] + is_artillery_storage[cell2] <= 1)
        if cell1 in is_artillery_storage and cell2 in is_high:
            model.AddImplication(is_artillery_storage[cell1], is_high[cell2].Not())
        if cell2 in is_artillery_storage and cell1 in is_high:
            model.AddImplication(is_artillery_storage[cell2], is_high[cell1].Not())

    threshold_people = model.NewIntVar(0, row_count * col_count * HIGH_DENSITY, "total_people")
    model.Add(threshold_people == sum(people[cell] for cell in cells))

    threshold_artillery = model.NewIntVar(0, row_count * col_count, "total_artillery")
    model.Add(threshold_artillery == sum(is_artillery_storage[cell] for cell in cells))

    model.Add(threshold_people <= PEOPLE_PER_STORE * threshold_artillery)
    model.Maximize(threshold_people)

    solver = cp_model.CpSolver()
    status = solver.solve(model)
    
    # Your code to make the dictionary that will be returned
    out = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for cell in cells:
            if solver.BooleanValue(is_artillery_storage[cell]):
                out[cell] = ("artillery", 0)
            elif solver.BooleanValue(is_high[cell]):
                out[cell] = ("high", solver.Value(people[cell]))
            else:
                out[cell] = ("low", LOW_DENSITY)
    return out