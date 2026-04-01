import numpy as np
import csv
from constants import CARDINALITY
import sys

if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} <input_file>")
    sys.exit(1)

input_path = sys.argv[1]

# Initialize data structures for counts
# (Include add-one smoothing!)
# Your code here
a =  CARDINALITY["A"]
b =  CARDINALITY["B"]
c =  CARDINALITY["C"]
d =  CARDINALITY["D"]

A = np.ones(a)
C = np.ones(c)
B = np.ones((a, b))
D = np.ones((b, c, d))

# Read all the rows of the data
with open(input_path, "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        # Convert entries to ints
        a = int(row["A"])
        b = int(row["B"])
        c = int(row["C"])
        d = int(row["D"])

        # Add them to the count
        # Your code here
        A[a] += 1
        C[c] += 1
        B[a, b] += 1
        D[b, c, d] += 1

# Make all the Conditional Probability Density tables
# (numpy arrays!)
cpd_a = A / A.sum()
cpd_b = B / B.sum(axis=1, keepdims=True)
cpd_c = C / C.sum()
cpd_d = D / D.sum(axis=2, keepdims=True)

print(f"A: {cpd_a.shape}")
print(f"B: {cpd_b.shape}")
print(f"C: {cpd_c.shape}")
print(f"D: {cpd_d.shape}")

# Save CPDs to a file
with open("cpds.npy", "wb") as f:
    np.save(f, cpd_a)
    np.save(f, cpd_b)
    np.save(f, cpd_c)
    np.save(f, cpd_d)
