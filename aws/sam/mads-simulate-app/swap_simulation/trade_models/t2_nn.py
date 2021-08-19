# t2_nn
import numpy as np
import pandas as pd
import torch
import pickle
import torch.nn as nn



class NNModelEx(nn.Module):
    def __init__(self, inputSize, outputSize, lookback_count, model_definition):
        super().__init__()

        network = []
        p = inputSize
        for k,v in model_definition:
            if k.startswith('l'):
                network.append(nn.Linear(in_features=p, out_features=v[0]))
                p=v[0]
            elif k.startswith('d'):
                network.append(nn.Dropout(v[0]))
            elif k.startswith('t'):
                network.append(nn.Tanh())
            elif k.startswith('s'):
                network.append(nn.Sigmoid())
            elif k.startswith('r'):
                network.append(nn.ReLU())

        if p != outputSize:
            network.append(nn.Linear(in_features=p, out_features=outputSize))

        self.net = nn.Sequential(*network)

    def forward(self, X):
        return self.net(X)

def columns(portfolio):
    static_columns = ['open']
    repeat_columns = ['high', 'low', 'close', 'rsi', 'trend_up3','trend_up14', 
                      'cs_ss','cs_ssr','cs_hm','cs_hmr','cs_ebu','cs_ebr']

    columns = static_columns + [f"{rc}_{i}" for rc in repeat_columns for i in range(0,24)]
    return columns

def make_decision(x_data, extra_data, info_dict):
    '''
    Returns decision wheter to buy (>0) / sell (<0) or hold (0), and the price to execute at.
            Parameters:
                    x_data (DataFrame): DataFrame of input data.  The index is a timestamp
                    extra_data (DataFrame): DataFrame with extra data, due to possibility of NaN values, dtypes may be incorrect
                    info_dict (dict): You can assign key and values to info_dict to pass data between batches

            Returns:
                    decision (Series): Series of decision values in the order the input x_data, index does not matter
                    execution_price (Series): Series of execution price in the order the input x_data, index does not matter
    '''    
    
    execution_price = x_data['close_0'].copy()

    if 'last_y' not in info_dict:
        info_dict['last_y'] = 0


    df = x_data.astype(float)
    for c in df.columns:
        if c.startswith("trend_up"):
            d = 'tc2x_' + c.replace('_up','')
            df[d] = (df[c] - 0.5) * 2
        elif c.startswith("rsi_"):
            df['tc2x_'+c] = (df[c] - 50) / 50
        elif c.startswith("high_") or c.startswith("low_") or c.startswith("close_"):
            df['tc2x_'+c] = ((df[c] / df['open']) - 1) * 30

    flag_pairs = [('tc2x_ss','cs_ss','cs_ssr'),('tc2x_hm','cs_hm','cs_hmr'),('tc2x_eb','cs_ebu','cs_ebr')]

    for newp,p1,p2 in flag_pairs:
         for i in range(0,24):
                df[f"{newp}_{i}"] = df[f"{p1}_{i}"] - df[f"{p2}_{i}"]

    df = df[[c for c in df.columns if c.startswith("tc2")]]

    nn_model = NNModelEx(216, 1, 24, [
        ('l', (600,)), ('r', (True,)),
        ('l', (600,)), ('r', (True,)),
        ('l', (600,)), ('r', (True,)),
        ('l', (600,)), ('r', (True,)),
        ('l', (600,)), ('r', (True,)),
        ('l', (600,)), ('r', (True,)),
        ('l', (600,)), ('r', (True,)),
        ('l', (1,)), ('r', (True,)),
    ])
    
    nn_model.load_state_dict(torch.load(info_dict['model_filepath']))
    
    nn_results = nn_model(torch.from_numpy(df.to_numpy()).float()).detach().numpy()

    decision = pd.Series(nn_results.reshape(-1), index=df.index)
    decision[(decision > info_dict['model_bs_ratio'][0]) & (decision < info_dict['model_bs_ratio'][1])] = 0.5
    decision = decision - 0.5
    
    return decision, execution_price
