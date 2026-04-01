import sys
from assign_purpose_a import assign_purpose
import pickle
from time import perf_counter

# Usage:
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <rows> <columns>")
    exit(-1)

row_count = int(sys.argv[1])
col_count = int(sys.argv[2])

start_time = perf_counter()

# Solve the CSP problem
assignments = assign_purpose(row_count, col_count)

stop_time = perf_counter()

print(f"Time: {(stop_time - start_time):f} seconds")

# Is it solved?
if assignments is None:
    print("Failed to solve")
else:
    # Show the results
    print(f"{len(assignments)} cells: {assignments}")

    # Save the results
    path = f"solution-{row_count}-{col_count}.pkl"
    with open(path, "wb") as outfile:
        pickle.dump(assignments, outfile)
    print(f"Wrote {path}.")
