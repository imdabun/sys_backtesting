"""
File: bktest.py
Backtest Class
CMU Algorithmic Trading Group (ATG) Systems Team
"""

import pandas as pd
import univ
import scheduler
import strat
import optimizer

class Backtest:
    """Backtest class that runs a single backtest using given parameters and strat lib"""
    OUT_LABELS = ["t_idx", "long_pnl", "short_pnl", "long_inst", "short_inst"]

    def __init__( self, btsettings: dict,
                        trade_scheduler: scheduler.TradeScheduler,
                        strat_lib: strat.StratLib,
                        portfolio_opt: optimizer.PortfolioOpt):
        self.btsettings = btsettings
        self.trade_scheduler = trade_scheduler
        self.strat_lib = strat_lib
        self.portfolio_opt = portfolio_opt
        self.output = []

        self.universe = None
        # create universe
        if self.btsettings['univ'] == 'custom':
            self.universe = univ.custom_univ(self.btsettings['start_time'],
                                        self.btsettings['burn_in'],
                                        self.btsettings['end_time'])
        else:
            self.universe = univ.create_univ(list(self.btsettings['univ']),
                                        self.btsettings['start_time'],
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
