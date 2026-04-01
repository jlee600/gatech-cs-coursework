import numpy as np
from numpy.typing import NDArray


# You are passed columns of training data, find the most likely value for the parameters:
#   "mu_a","std_a" are the mean and standard deviation of the area (which is normally distributed)
#   "lambda_v" is the mean of visitor count (which is Poisson distributed)
#   "s" is the probability of true (which is Bernoulli distribted)
def make_parameters(
    areas: NDArray[np.float64],
    visitors1: NDArray[np.float64],
    visitors2: NDArray[np.float64],
    felons: NDArray[bool],
):
    # Get the important stats
    mu_a = float(np.mean(areas))
    std_a = float(np.std(areas)) 
    ## Your code here
    lambda_v = float(np.mean(np.concatenate((visitors1, visitors2))))
    s = float(np.mean(felons))

    # Put them in an array (standard deviation, not variance!)
    return {"mu_a": mu_a, "std_a": std_a, "lambda_v": lambda_v, "s": s}
