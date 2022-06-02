"""
File: univ.py
Universe Class and universe creation functions
CMU Algorithmic Trading Group (ATG) Systems Team
"""

import numpy as np

class Universe:
    """
    Universe class encapsulating information of the instruments needed for a backtest run
    """

    def info ( self):
        """
        Displays a description of the universe
        """
        raise NotImplementedError

    def forward( self, t_idx: int, alpha: np.ndarray)-> np.ndarray:
        """
        Takes in time index and alpha array, returns the PnL calculation from last t_idx to current
        """
        raise NotImplementedError

    def burnin_status( self)-> bool:
        """
        Returns whether the burn-in period is complete and testing phase can begin
        """
        raise NotImplementedError


def create_univ(tags: list, 
                start_time: int,
                burn_in: int,
                end_time: int )-> Universe:
    """"
    Creates a standard universe based on the tags, which is a char list
    Character for type of instrument:
    c     Currency
    f     Forwards and Futures
    o     Options
    p     Perpetual Contracts
    s     Swaps
    """
    return # TODO


def custom_univ(start_time: int, burn_in: int, end_time: int)-> Universe:
    """
    [USER IMPLEMENTED] Custom universe which has to take in the 3 arguments
    """
    raise NotImplementedError
