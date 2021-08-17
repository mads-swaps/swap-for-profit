import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from IPython.display import display


def columns(portfolio):
    return ['close']

def initalize(x_data, info_dict):
    '''
    initialize parameters
    '''

    info_dict['lags'] = 3
    info_dict['train_test_ratio'] = 0.7
    # info_dict['data_size'] = 100
    info_dict['results'] = None
    info_dict['model'] = linear_model.LogisticRegression(C=1e6,
                solver='lbfgs', multi_class='ovr', max_iter=1000)

    info_dict['start'] = x_data.index[0]
    # info_dict['end'] = x_data.index[info_dict['portfolio']['data_size']]
    info_dict['end'] = x_data.index[-1]

    info_dict['start_in'] = info_dict['start']
    e_in = int(info_dict['train_test_ratio'] * len(x_data.index))
    info_dict['end_in'] = x_data.index[e_in]

    info_dict['start_out'] = x_data.index[e_in + 1]
    info_dict['end_out'] = info_dict['end']

    return get_data(x_data, info_dict)

def get_data(x_data, info_dict):
    '''
    prepares the data.
    '''
    # print("get data====")
    x_data = x_data.loc[info_dict['start']:info_dict['end']]
    # print(f"xdata:\n{x_data.head(2)}")
    x_data['returns'] = np.log(x_data['close'] / x_data['close'].shift(1))
    x_data = x_data.dropna()
    # print(f"xdata:\n{x_data.head(2)}")
    # print(f"len(xdata):{len(x_data)}")
    return x_data

def select_data(start, end, x_data, info_dict):
    '''
    Selects sub-sets of the financial data.
    '''

    # print("select data====")
    data = x_data[(x_data.index >= start) & (x_data.index <= end)].copy()
    # print(f"data:\n{data.head(2)}")
    # print(f"len(data):{len(data)}")
    return data

def prepare_features(start, end, x_data, info_dict):
    '''
    Prepares the feature columns for the regression and prediction steps.
    '''
    # print("prepare features====")
    info_dict['data_subset'] = select_data(start, end, x_data, info_dict)
    # print(info_dict['data_subset'].head(2))
    info_dict['feature_columns'] = []
    for lag in range(1, info_dict['lags'] + 1):
        col = 'lag_{}'.format(lag)
        info_dict['data_subset'][col] = info_dict['data_subset']['returns'].shift(lag)
        info_dict['feature_columns'].append(col)
    info_dict['data_subset'].dropna(inplace=True)

    # print(f"data_subset:\n{info_dict['data_subset'].head(2)}")
    # print(f"len(data_subset):{len(info_dict['data_subset'])}")

def fit_model(x_data, info_dict):
    '''
    Implements the fitting step.
    '''
    prepare_features(info_dict['start_in'], info_dict['end_in'], x_data, info_dict)
    info_dict['model'].fit(info_dict['data_subset'][info_dict['feature_columns']],
                    np.sign(info_dict['data_subset']['returns']))


def plot_results(info_dict):
    '''
    Plots the cumulative performance of the trading strategy
    compared to the symbol.
    '''
    if info_dict['results'] is None:
        print('No results to plot yet. Run a strategy.')
    title = f'{info_dict["portfolio"]["starting_coin"]}-{info_dict["portfolio"]["pair_coin"]} | \
                        TC = {info_dict["portfolio"]["trading_fees_percent"]:.4f}'

    info_dict['results'][['cum_returns', 'equity_curve']].plot(title=title, figsize=(10, 6))


def make_decision(x_data, extra_data, info_dict):
    '''
    Description...

    Parameters:

    Returns:
        decision (Series): Series of decision values in the order the input x_data, index does not matter
        execution_price (Series): Series of execution price in the order the input x_data, index does not matter
    '''

    # initialization
    x_data = initalize(x_data, info_dict)
    # start the logic
    fit_model(x_data, info_dict)
    prepare_features(info_dict['start_out'], info_dict['end_out'], x_data, info_dict)
    prediction = info_dict['model'].predict(info_dict['data_subset'][info_dict['feature_columns']])
    info_dict['data_subset']['prediction'] = prediction
    info_dict['data_subset']['strategy'] = (info_dict['data_subset']['prediction'] * info_dict['data_subset']['returns'])
    # print("====")
    # print(f"len(prediction):{len(info_dict['data_subset']['prediction'])}")
    # print(f"len(strategy):{len(info_dict['data_subset']['strategy'])}")
    # print(f"len(xdata):{len(x_data['close'])}")

    # determine when a trade takes place
    trades = info_dict['data_subset']['prediction'].diff().fillna(0) != 0

    # subtract transaction costs from return when trade takes place
    info_dict['data_subset']['strategy'][trades] -= info_dict['portfolio']['trading_fees_percent']
    
    info_dict['data_subset']['cum_returns'] = (info_dict['portfolio']['starting_funds'] *
                                               info_dict['data_subset']['returns'].cumsum().apply(np.exp))

    info_dict['data_subset']['equity_curve'] = (info_dict['portfolio']['starting_funds'] *
                                                info_dict['data_subset']['strategy'].cumsum().apply(np.exp))

    info_dict['results'] = info_dict['data_subset']

    print("data subset before return:============")
    display(info_dict['data_subset'])

    # print("unique pred values:===================")
    # display(info_dict['data_subset']['prediction'].unique())

    # display(info_dict['results'].head(2))

    plot_results(info_dict)

    return info_dict['data_subset']['prediction'], info_dict['data_subset']['close']