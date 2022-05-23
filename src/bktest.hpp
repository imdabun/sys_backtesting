/*  File: bktest.hpp
 *  Header file for main bktest operation
 *  CMU Algorithmic Trading Group (ATG) Systems Team
 */

#pragma once

#include <utility>
#include <iostream>
#include <string>
#include <map>

enum Instval { LONG, SHORT, INVAL };

typedef long t_idx;
typedef std::vector<double> alpha;
typedef std::vector<Instval> inst;

namespace Backtest_env {

  class BTSettings {
  // Contains all settings of a particular run of the backtesting algorithm
  private:

    std::vector<std::map<std::string, void*> > params;

  public:

    BTSettings() {};

    // We need a custom destructor to free the void* in the maps of params properly
    ~BTSettings() {};

  };

  class Universe {
  // From database build a universe of instruments, accounting for events like stock splits, etc.
  private:

    bool warmup;

  public:

    Universe() {};

    virtual void init( const BTSettings& btsettings, int run_idx) {};

    virtual std::pair<alpha, inst> foward( t_idx, alpha ) {};

    bool wmp_status() {};

  };  

  class Trade_Scheduler {
  // Schedules when each new trade update is called
  private:

  public:

    Trade_Scheduler() {};

    virtual void init( const BTSettings& btsettings, int run_idx) {};

    t_idx update() {};

  };

  class Portfolio_Opt {
  // Portfolio Optimizer, keeps track of past weight vectors and adjusts weights to constraints
  private:

  public:

    Portfolio_Opt() {};

    virtual void init( const BTSettings& btsettings, int run_idx) {};

    virtual alpha forward( t_idx, alpha ) {};

  };

  class Strategy {
  // Parent class for new strategies to inherit from
  private:

  public:

    Strategy() {};

    virtual alpha forward( t_idx ) {};

  };

  class Strat_Lib {
  // Container class for algorithms
  private:
  
    std::vector<Strategy> lib;

  public:

    Strat_Lib() {};

    alpha forward( t_idx ) {};

  };

  class Backtest {
  // Main backtest object that runs test, keeps track of past results, outputs metrics
  private:

    std::vector<bool> status;

    std::map<std::string, double> hyperparams;

    std::vector<std::vector> > out;

    std::vector<std::map<std::string, double> > inst_out;

  public:

    /*  Constructor: Backtest
     *  Inputs:
     *    hyperparams     A map to hyperparameters and their initial values
     *    btsettings      BTSettings object containing all settings for the backtest
     *    alpha_factor    Alpha_Factor object that assigns weights to strategies in Strat_Lib
     *    trade_scheduler Trade_Scheduler object that calls the appropriate update timestamps
     *    portfolio_opt   Portfolio_Opt object that converts alpha factors to actual portfolio allocation
     *    strat_lib       Strat_Lib object that contains a library of all the strategies used in backtest
     */
    Backtest( std::map<std::string, double> hyperparams,
              BTSettings btsettings, 
              Alpha_Factor alpha_factor,
              Trade_Scheduler trade_scheduler,
              Portfolio_Opt portfolio_opt,
              Strat_Lib strat_lib,
              ) {}; 

    friend std::ostream operator<<(std::ostream& os, const Backtest& bktest);

    /*  Method: run       Function to run backtest and save outputs 
     *  Inputs:
     *    hyperparams     A map to hyperparameters and their initial values
     *    btsettings      BTSettings object containing all settings for the backtest
     *    alpha_factor    Alpha_Factor object that assigns weights to strategies in Strat_Lib
     *    trade_scheduler Trade_Scheduler object that calls the appropriate update timestamps
     *    portfolio_opt   Portfolio_Opt object that converts alpha factors to actual portfolio allocation
     *    strat_lib       Strat_Lib object that contains a library of all the strategies used in backtest
     *  Output:
     *    int             Number for debugging and exception purposes
     *  Effect:
     *    updates out and/or inst_out
     *  Pseudocode:
     *    for each backtest run:
     *      initialize universe (taking params from BTSettings) in particular, initialize warmup condition
     *      initialize trade_scheduler (taking params from BTSettings)
     *      initialize portfolio_opt (taking params from BTSettings)
     *      for each scheduled_update called by trade_scheduler:
     *        (note that scheduled_update contains an index object we can use with universe to calculate PnL per update)
     *        (this index object, say update_index, is universal across most data types such that calling the same index will retrieve latest data at index timestamp)
     *        call strategy.forward(update_index) for each strategy in strat_libs (done in alpha_factor.forward)
     *        call portfolio_opt.forward(update_index, alpha) to get a cumulative trades vector (trades)
     *        call universe.forward(update_index, trades) to get inst_pnl vector and valid_inst vector
     *        (valid_inst will indicate at each index if the instrument is long, short or invalid, using enum type Instval)
     *        Use inst_pnl and valid_inst to calculate outputs
     *        if universe.wmp_status() period over, save outputs
     */
    int run() {};

    /*  Method: dump      Function to dump outputs
     *  Inputs:
     *    -
     *  Output:
     *    -
     *  Effect:
     *    dumps out and/or inst_out based on BTSettings
     */    
    void dump() {};

  }; 

}

/*

Users
- Implement BTSettings, treating it as a giant dictionary of sorts
  (the main usage of BTSettings is to store a map mapping parameters for each run)
- Either use one of the defaults, or implement your own version of Alpha_Factor, Trade_Scheduler and/or Portfolio_Opt
- Implement any new strategies
- Implement Strats_Lib which is a container of all the strategies used in a single backtest

Default Options
> Universe defaults
  Character for type of instrument:
  c     Currency
  f     Forwards and Futures
  o     Options
  p     Perpetual Contracts
  s     Swaps
  A universe made up of multiple types of instruments combined is declared by concatenating them in alphabetical order 
  e.g. a currency + options universe is declared as Crypto("co")

> Trade_Scheduler defaults
  Update every 5, 10, 20, 60 minutes
  Update per X volume traded (where x is provided as a parameter)

> Alpha_Factor defaults
  Equal Weightage

> Portfolio_Opt defaults
  No optimization
  Linear and Exponential decay with parameter (decay period)

*/