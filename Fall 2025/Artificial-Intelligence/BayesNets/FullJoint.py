import numpy as np

class FullJoint:
    def __init__(self, filename):
        with open(filename, "rb") as f:
            self.cpd_a = np.load(f)
            self.cpd_b = np.load(f)
            self.cpd_c = np.load(f)
            self.cpd_d = np.load(f)

    def likelihood(self, a, b, c, d):
        # Your code here
        return self.cpd_a[a] * self.cpd_b[a, b] * self.cpd_c[c] * self.cpd_d[b, c, d]
