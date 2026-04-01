import sys
from FullJoint import FullJoint

if len(sys.argv) != 5:
    print(f"Usage:python3 {sys.argv[0]} <a> <b> <c> <d>")
    exit(-1)

full_joint = FullJoint("cpds.npy")

a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])
d = int(sys.argv[4])

likelihood = full_joint.likelihood(a, b, c, d)
print(f"Likelihood of observing A={a}, B={b}, C={c}, D={d}: {likelihood}")
