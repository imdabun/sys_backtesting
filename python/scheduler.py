"""
File: scheduler.py
StratScheduler and TradeScheduler Classes
CMU Algorithmic Trading Group (ATG) Systems Team
"""

from typing import Tuple, Generator
import univ

class StratScheduler:
    """Strategy Scheduler class that schedules alpha update timings for one strategy"""

    def __init__( self):
        """
        Creates StratScheduler object
        """
        self.universe = None

    def info ( self):
        """
        [USER IMPLEMENTED] Displays a description of the scheduler
        """
        raise NotImplementedError

    def univ( self, universe: univ.Universe):
        """
        Method to select the universe for the scheduler
        """
        self.universe = universe

    def update( self)-> int:
        """
        [USER IMPLEMENTED] A generator that yields the next t_idx
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

    def univ( self, universe: univ.Universe):
        """
        Method to select the universe for the scheduler
        """
        for strat in self.strat_schedulers:
            strat.univ(universe)

    def update( self)-> Tuple[str, int]:
        """
        [USER IMPLEMENTED] A generator that yields the tuple (strat_dict, t_idx)
        Here strat_dict is a dictionary of all strategies to be updated
        """
        raise NotImplementedError

    def update_all( self)-> Generator[int]:
        """
        [USER IMPLEMENTED] A generator that yields t_idx to update all strategies
        """
        raise NotImplementedError


class FixedTime(StratScheduler):
    """A scheduler that updates on every fixed [lag] units of time"""

    def __init__( self, lag):
        """
        Takes the update lag parameter
        """
        super().__init__()
        self.lag = lag

    def info( self):
        print("Scheduler that updates every [lag] units of time")

    def update( self):
        for i in range(self.universe.start_time, self.universe.end_time, self.lag):
            yield i
