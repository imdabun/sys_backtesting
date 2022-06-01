"""
File: bktest.py
Python base class declarations for bktest system
CMU Algorithmic Trading Group (ATG) Systems Team
"""

import numpy as np
import pandas as pd

class Universe:
    """
    Universe class encapsulating information of the instruments needed for a backtest run
    Character for type of instrument:
    c     Currency
    f     Forwards and Futures
    o     Options
    p     Perpetual Contracts
    s     Swaps
    """

    def info ( self ):
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


class StratScheduler:
    """Strategy Scheduler class that schedules alpha update timings for one strategy"""

    def info ( self ):
        """
        Displays a description of the scheduler
        """
        raise NotImplementedError

    def univ( self, universe: Universe ):
        """
        Method to select the universe for the scheduler
        """
        self.universe = universe

    def update( self)-> int:
        """
        A generator that yields the next t_idx as it is called
        """
        raise NotImplementedError


class TradeScheduler:
    """Trade Scheduler class that schedules trade update timings for all strategies"""

    def __init__( self, strat_schedulers: dict):
        """
        Takes in a dictionary of strategy schedulers with the same universe
        """
        self.strat_schedulers = strat_schedulers
        self.universe = None

    def univ( self, universe: Universe ):
        """
        Method to select the universe for the scheduler
        """
        for strat in self.strat_schedulers:
            strat.univ(universe)

    def update( self )-> '(str, int)':
        """
        A generator that yields the tuple (strat_dict, t_idx) as it is called
        Here strat_dict is a dictionary of all strategies to be updated
        """
        raise NotImplementedError

    def update_all( self )-> 'int generator':
        """
        A generator that yields t_idx to update all strategies
        """
        raise NotImplementedError


class Strategy:
    """Alpha class that describes alpha signal/trading logic"""

    def info ( self ):
        """
        Displays a description of the strategy
        """
        raise NotImplementedError

    def univ( self, universe: Universe ):
        """
        Method to select the universe for the strategy
        """
        self.universe = universe

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

    def univ( self, universe: Universe ):
        """
        Method to select the universe for all strategies
        """
        for strat in self.lib:
            self.lib[strat].univ(universe)

    def forward( self, strats: dict, t_idx: int)-> None:
        """
        The trade function called on a specific strat
        >> Have to think about how to implement it most efficiently 
        >> What if we want to update a subset of strategies at the same time 
        """
        for strat in strats:
            self.alphas[strat] = self.lib[strat].forward(t_idx)

    def forward_all( self, t_idx: int)-> None:
        """
        The trade function called on the entire library of signals
        """
        for strat in self.lib:
            self.alphas[strat] = self.lib[strat].forward(t_idx)


class PortfolioOpt:
    """Portfolio Optimizer class that combines and optimizes a portfolio based
    on alpha signals in the strat library"""

    def info ( self ):
        """
        Displays a description of the portfolio optimizer
        """
        raise NotImplementedError

    def forward( self, t_idx: int, strat_lib: StratLib) -> np.ndarray:
        """
        Function that calculates values to assign to instruments based on
        signals in the strat library
        """
        raise NotImplementedError


class Backtest:
    """Backtest class that runs a single backtest using given parameters and strat lib"""
    OUT_LABELS = ["t_idx", "long_pnl", "short_pnl", "long_inst", "short_inst"]

    def __init__( self, btsettings: dict, # universe, start_time, burn_in, end_time
                        trade_scheduler: TradeScheduler,
                        strat_lib: StratLib,
                        portfolio_opt: PortfolioOpt ):
        self.btsettings = btsettings
        self.trade_scheduler = trade_scheduler
        self.strat_lib = strat_lib
        self.portfolio_opt = portfolio_opt
        self.output = []

        self.universe = None
        # create universe
        if self.btsettings['univ'] == 'custom':
            self.universe = custom_univ( self.btsettings['start_time'],
                                    self.btsettings['burn_in'],
                                    self.btsettings['end_time'])
        else:
            self.universe = create_univ( self.btsettings['start_time'],
                                    self.btsettings['burn_in'],
                                    self.btsettings['end_time'])
        self.trade_scheduler.univ(self.universe)
        self.strat_lib.univ(self.universe)
        self.portfolio_opt.univ(self.universe)

    def run(self):
        """
        Main function to run the backtest
        """
        if self.btsettings['sync_schedule']:
            # synchronized scheduler updates for all
            for t_idx in self.trade_scheduler.update_all():
                self.strat_lib.forward_all(t_idx)
                alpha_vec = self.portfolio_opt.forward(t_idx, self.strat_lib)
                out_vec = self.universe.forward(t_idx, alpha_vec)
                if not self.universe.burnin_status():
                    self.output.append(out_vec)
        else:
            # desynchronized scheduling; i.e. at each t_idx only a subset updated
            for strats, t_idx in self.trade_scheduler.update():
                self.strat_lib.forward(strats, t_idx)
                alpha_vec = self.portfolio_opt.forward(t_idx, self.strat_lib)
                out_vec = self.universe.forward(t_idx, alpha_vec)
                if not self.universe.burnin_status():
                    self.output.append(out_vec)

    def dump(self, **kwargs):
        """
        Dump the output dataframe saved after running the backtest
        """
        data_frame = pd.DataFrame(data=self.output, columns=self.OUT_LABELS)
        data_frame.to_csv(**kwargs)
