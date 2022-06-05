"""
File: strat.py
Strategy and StratLib Classes
CMU Algorithmic Trading Group (ATG) Systems Team
"""

import numpy as np
import univ

class Strategy:
    """Alpha class that describes alpha signal/trading logic"""

    def info ( self):
        """
        [USER IMPLEMENTED] Displays a description of the strategy
        """
        raise NotImplementedError

    def univ( self, universe: univ.Universe):
        """
        Method to select the universe for the strategy
        """
        self.universe = universe

    def forward( self, t_idx: int)-> np.ndarray:
        """
        [USER IMPLEMENTED] The trade function of a particular strategy/alpha
        signal; takes in the time index and returns alpha array
        """
        raise NotImplementedError


class StratLib:
    """Container class for strategies"""

    def __init__( self, lib):
        """
        Initialize with dictionary of strategies
        """
        self.lib = lib
        self.alphas = {}

    def univ( self, universe: univ.Universe ):
        """
        Method to select the universe for all strategies
        """
        for strat in self.lib:
            self.lib[strat].univ(universe)

    def forward( self, strats: dict, t_idx: int)-> None:
        """
        The trade function called on a specific strat
        """
        for strat in strats:
            self.alphas[strat] = self.lib[strat].forward(t_idx)

    def forward_all( self, t_idx: int)-> None:
        """
        The trade function called on the entire library of signals
        """
        for strat in self.lib:
            self.alphas[strat] = self.lib[strat].forward(t_idx)
