import numpy as np
from typing import List, Tuple
import numpy.typing as npt
from scipy.stats import nbinom, beta
import math

# Constants
SLICE_COUNT = 1000
ALPHA = 5
BETA = 3


class CoinEstimator:
    def prepare_to_estimate(self, experiments: List[Tuple[int, int]]):
        # Compute the probability distribution for the coin given the
        # experiments. It should be a numpy array of shape (SLICE_COUNT,)

        ## Your code here
        theta = (np.arange(0, SLICE_COUNT) + 0.5) / SLICE_COUNT
        prior = beta.logpdf(theta, ALPHA, BETA)
        
        like = np.zeros(SLICE_COUNT, dtype=float)
        for r, w in experiments:
            fail = w - r
            like += nbinom.logpmf(fail, r, theta)
        post = prior + like
        
        m = np.max(post)
        post = np.exp(post - m)
        post /= np.sum(post)

        self.pdf = post

    def max_a_posteriori(self) -> float:
        best_slice = np.argmax(self.pdf)
        return best_slice / SLICE_COUNT

    def probability_density(self, x) -> float:
        slice = int(x * SLICE_COUNT)
        return self.pdf[slice]

    def credibility_interval(self, s: float) -> Tuple[float, float]:

        # Compute the smallest interval with credibility 's'

        ## Your code here
        pdf = self.pdf.copy()                 
        n = len(pdf)
        order = np.argsort(pdf)[::-1]

        thresh = 0.0
        min_i = n
        max_i = -1

        for idx in order:
            thresh += pdf[idx]
            if idx < min_i: 
                min_i = idx
            if idx > max_i: 
                max_i = idx
            if thresh >= s:
                break

        return min_i / SLICE_COUNT, (max_i + 1) / SLICE_COUNT
