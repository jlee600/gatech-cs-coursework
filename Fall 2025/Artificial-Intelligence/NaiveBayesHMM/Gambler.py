import numpy as np
from numpy.typing import ArrayLike, NDArray


class Gambler:

    def __init__(
        self,
        dice: NDArray[np.float64],
        payout: NDArray[np.float64],
        transitions: NDArray[np.float64],
        initial: NDArray[np.float64],
    ):
        # Note the arguments that were passed in
        self.dice = dice
        self.payout = payout
        self.transitions = transitions
        self.initial = initial

        # Cache this -- you will need it a lot
        self.expected_winnings_for_each_die = np.dot(self.dice, self.payout)

        # Your belief about what die is being used on the next roll
        # This will be updated after every roll
        self.state_p = initial.copy()

    # Current beliefs about the probability that each die is about to be rolled
    # Used by the autograder
    def current_beliefs(self) -> NDArray[np.float64]:
        return self.state_p

    # Assume Markov Chain is ergodic, return the stationary_distribution
    def stationary_distribution(self) -> NDArray[np.float64]:
        ## Your code here
        evals, evecs = np.linalg.eig(self.transitions.T)
        idx = np.argmin(np.abs(evals - 1.0))
        stationary_vec = np.real(evecs[:, idx])
        return stationary_vec / np.sum(stationary_vec)

    # Average winnings for each roll of each die
    def expected_winnings_by_die(self) -> NDArray[np.float64]:
        return self.expected_winnings_for_each_die

    # If you bet on every roll, what would you expect your average
    # winnings per roll to be?
    def expected_winnings_per_roll_bet_every_roll(self) -> np.float64:
    ## Your code here
        return np.dot(self.stationary_distribution(), self.expected_winnings_for_each_die)

    # If the croupier told you what die he was using, what would you expect your average
    # winnings per roll to be? (Include in "per roll" all the rolls, not just the ones you would bet on.)
    def expected_winnings_per_roll_bet_on_good_dice(self) -> np.float64:
    ## Your code here
        temp = self.expected_winnings_for_each_die * (self.expected_winnings_for_each_die > 0)
        return np.dot(self.stationary_distribution(), temp)

    def will_bet(self) -> bool:
        # Assuming I am right about the state_p, what should I expect to win?
        expected_winning = np.dot(self.expected_winnings_for_each_die * self.state_p, np.ones(len(self.state_p)))

        # If that is positive, I will bet
        return expected_winning > 0.0

    # The croupier just rolled a 'side'
    # Update your beliefs
    def update(self, side: int):
    ## Your code here
        temp = self.dice[:, side]
        old = self.state_p * temp
        new = np.dot(old, self.transitions)
        self.state_p = new / np.sum(new)
