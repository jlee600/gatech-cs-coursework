import itertools
import numpy as np
from typing import List
import numpy.typing as npt


class LongBelief:
    def __init__(self, die_count: int, die_sides: int):

        # Hold on to the arguments
        self.die_count = die_count
        self.die_sides = die_sides

        # Compute the log priors for all possible rolls
        # Replace any prior that would have been zero with
        # a logprior of -np.inf

        ## Your code here
        max_sum = self.die_sides * self.die_count
        min_sum = self.die_count

        prior = np.zeros(max_sum + 1, dtype=float)
        for outcome in itertools.product(range(1, self.die_sides + 1), repeat=self.die_count):
            prior[sum(outcome)] += 1.0
        prior /= np.sum(prior)

        logprior = np.log(prior, where= prior > 0)
        logprior[prior == 0] = -np.inf
    
        self.logpriors = logprior
        # self.show_array(self.logpriors, "log P(d)")

        # Create a dictionary with the keys being "H", "L", or "E"
        # The values will be numpy arrays of log probabilitiesof the key given each possible roll

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

        h_loglikelihoods = np.log(h, where= h > 0)
        h_loglikelihoods[h == 0] = -np.inf

        e_loglikelihoods = np.log(e, where= e > 0)
        e_loglikelihoods[e == 0] = -np.inf

        l_loglikelihoods = np.log(l, where= l > 0)
        l_loglikelihoods[l == 0] = -np.inf

        # Put them in a dictionary for easy lookup
        self.log_letter_likelihoods = {
            "H": h_loglikelihoods,
            "L": l_loglikelihoods,
            "E": e_loglikelihoods,
        }

        # for key, value in self.letter_likelihoods.items():
        #     self.show_array(value, f"log P({key}|d)")

    def show_array(self, array, label):
        print(f"{label:>13}| ", end="")
        for i in range(self.die_count, self.die_sides * self.die_count + 1):
            print(f"{i}:{array[i]:.3f} ", end="")
        print()

    def analyze(self, letters: List[str]) -> npt.ArrayLike:
        # Compute the posterior probabiliy given the sequence of letters
        ## Your code here
        posterior = self.logpriors.copy()
        for letter in letters:
            posterior += self.log_letter_likelihoods[letter]
        
        m = np.max(posterior)
        posterior = np.exp(posterior - m)
        posterior /= np.sum(posterior)
    
        return posterior
