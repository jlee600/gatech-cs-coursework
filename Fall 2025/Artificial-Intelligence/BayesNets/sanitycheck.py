from FullJoint import FullJoint
import itertools
import constants

domains = []
for k in constants.KEYS:
    domains.append(range(constants.CARDINALITY[k]))

all_combinations = itertools.product(*domains)

full_joint = FullJoint("cpds.npy")

sum = 0.0
for combo in all_combinations:
    p = full_joint.likelihood(*combo)
    print(f"p{combo} = {p * 100.0:.5f} %")
    sum += p

print(f"Total: {sum}, should be about 1.0")
