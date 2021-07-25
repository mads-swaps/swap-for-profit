# tc_0_dummy
import numpy as np
import pandas as pd

def columns():
    return ['open', 'close']

def make_decision(x_data, info_dict):
    # you can assign key and values to info_dict to pass data between batches
    # ie: if you do info_dict['test'] = 'testing', next batch will have access to info_dict['test']
    # portfolio is provided by default
    
    # Init variables for this batch
    if 'batch_num' not in info_dict:
        info_dict['batch_num'] = 0 # start at 0
        info_dict['last_action_index'] = 0
    last_action = info_dict['last_action_index'] - (info_dict['batch_num'] * info_dict['portfolio']['max_batch_size']) # will be negative if last action was from previous batch

    
    # Remember to do scaling or normalization here if needed. x_data is not scaled or normalized
    
    delta = x_data['close'] - x_data['open']
    
    decision = pd.Series(0, index=x_data.index) # hold
    decision = decision.where(delta > x_data['open'] * 0.005, 1) # buy if close is went up more than 0.5%
    decision = decision.where(-delta > x_data['open'] * 0.005, -1) # sell if close is went down more than 0.5%
    
    # now I want to add a restriction that if I bought or sold, I will hold for at least 8 candles
    # I'll go back and change buy/sell decisions if they are within 8 candles of last buy/sell
    
    # Enumerating is slow, so if you can just use vectorization, the simulation will run much faster
    cooldown_period = 8
    for i, (k,v) in enumerate(decision.items()):
        if last_action + cooldown_period > i:
            decision[k] = 0 # set to hold
        elif v !=0: # else if not hold
            last_action = i
            
    return decision