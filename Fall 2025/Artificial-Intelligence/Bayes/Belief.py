import itertools
import numpy as np
from typing import List
import numpy.typing as npt


class Belief:
    def __init__(self, die_count: int, die_sides: int):
        self.die_count = die_count
        self.die_sides = die_sides

        # Create a numpy array of prior probabilities for each possible roll
        # Make it of length die_sides * die_count + 1

        ## Your code here
        max_sum = self.die_sides * self.die_count
        min_sum = self.die_count

        prior = np.zeros(max_sum + 1, dtype=float)
        for outcome in itertools.product(range(1, self.die_sides + 1), repeat=self.die_count):
            prior[sum(outcome)] += 1.0
        prior /= np.sum(prior)

        self.priors = prior
        # self.show_array(self.priors, "P(d)")

        # Create a dictionary with the keys being "H", "L", or "E"
        # The values will be numpy arrays of probabilities of the key given each possible roll

        ## Your code here
        cdf = np.cumsum(prior)
        # P(E|d) = 1
        e = prior.copy()
        # p(H|d) = P(x > d) = 1 - P(x <= d) = 1 - CDF(d)
        h = 1.0 - cdf
        h = np.clip(h, 0.0, 1.0)  
        # P(L|d) = P(x < d) = CDF(d - 1)
        l = cdf.copy()
        l[0] = 0.0
        l[1:] = cdf[:-1]

        self.letter_likelihoods = {"H": h, "L": l, "E": e}

        # for key, value in self.letter_likelihoods.items():
        #     self.show_array(value, f"P({key}|d)")

    def show_array(self, array, label):
        print(f"{label:>13}| ", end="")
        for i in range(self.die_count, self.die_sides * self.die_count + 1):
            print(f"{i}:{array[i]:.3f} ", end="")
        print()

    def analyze(self, letters: List[str]) -> npt.ArrayLike:

        # Compute the posterior probabilities

        ## Your code here`
        posterior = self.priors.copy()
        for letter in letters:
            likelihoods = self.letter_likelihoods[letter]
            # P(d|letters) = P(letters|d) * P(d) / P(letters)
            posterior *= likelihoods
            p_letter = np.sum(posterior)
            posterior /= p_letter
        return posterior
