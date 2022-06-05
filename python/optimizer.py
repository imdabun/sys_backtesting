"""
File: optimizer.py
PortfolioOpt Class
CMU Algorithmic Trading Group (ATG) Systems Team
"""

import numpy as np
import strat

class PortfolioOpt:
    """Portfolio Optimizer class that combines and optimizes a portfolio based
    on alpha signals in the strat library"""

    def info ( self ):
        """
        Displays a description of the portfolio optimizer
        """
        raise NotImplementedError

    def forward( self, t_idx: int, strat_lib: strat.StratLib) -> np.ndarray:
        """
        [USER IMPLEMENTED] Function that calculates values to assign to
        instruments based on signals in the strat library
        """
        raise NotImplementedError

class NormSum(PortfolioOpt):
    """Portfolio Optimizer that simply adds all normalized signals"""

    def info (self):
        print("Portfolio Optimizer that simply adds all normalized signals")

    def forward(self, t_idx, strat_lib):
        pass # TODO
