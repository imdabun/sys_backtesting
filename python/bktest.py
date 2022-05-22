"""
File: bktest.py
Python base class declarations for bktest system
CMU Algorithmic Trading Group (ATG) Systems Team
"""

import numpy as np

class Universe:
    """Universe class encapsulating information of the instruments needed for a backtest run"""

    def forward( self, t_idx: int, alpha: np.ndarray)-> np.ndarray:
        """
        Takes in time index and alpha array, returns the PnL calculation from last t_idx to current
        """
        raise NotImplementedError

    def wmp_status( self)-> bool:
        """
        Returns whether the warmup period is complete and testing phase can begin
        """
        raise NotImplementedError


class StratScheduler:
    """Strategy Scheduler class that schedules alpha update timings for one strategy"""

    def update( self)-> int:
        """
        A generator that yields the next t_idx as it is called
        """
        raise NotImplementedError


class TradeScheduler:
    """Trade Scheduler class that schedules trade update timings for all strategies"""

    def __init__( self, strat_schedulers: dict):
        """
        Takes in a dictionary of strategy schedulers
        """
        self.strat_schedulers = strat_schedulers

    def update( self)-> int:
        """
        A generator that yields the next t_idx as it is called
        """
        raise NotImplementedError


class Strategy:
    """Alpha class that describes alpha signal/trading logic"""

    def forward( self, t_idx: int)-> np.ndarray:
        """
        The trade function of a particular strategy/alpha signal; takes in the
        time index and returns alpha array
        """
        raise NotImplementedError


class StratLib:
    """Container class for strategies"""

    def __init__( self):
        """
        Initialize with dictionary of strategies
        """
        self.lib = {}
        self.alphas = {}

    def forward_all( self, t_idx: int)-> None:
        """
        The trade function called on the entire library of signals
        """
        pass # TODO


class PortfolioOpt:
    """Portfolio Optimizer class that combines and optimizes a portfolio based
    on alpha signals in the strat library"""

    def forward( self, t_idx: int, strat_lib: StratLib) -> np.ndarray:
        """
        Function that calculates values to assign to instruments based on
        signals in the strat library
        """
        raise NotImplementedError


class Backtest:
    """Backtest class that runs a single backtest using given parameters and strat lib"""

    def __init__( self, btsettings: dict, 
                        trade_scheduler: TradeScheduler,
                        strat_lib: StratLib,
                        portfolio_opt: PortfolioOpt,):
        pass # TODO

    def run(self):
      
        pass # TODO

    def dump(self):

        pass # TODO