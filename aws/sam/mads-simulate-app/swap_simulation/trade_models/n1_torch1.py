import numpy as np
import pandas as pd
import pickle
import torch
from .n1_torch1_dataset import Dataset, to_device
from .n1_torch1_model import ResNet28


def columns(portfolio):
    lookback_days = portfolio.get('model_lookback_days',0)

    if lookback_days == 14:
        return ['open', 'high', 'low', 'close', 'dow', 'tod', 'number_of_trades', 'volume', 'quote_asset_volume', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ma14', 'ma30', 'ma90', 'sup14', 'sup30', 'sup90', 'res14', 'res30', 'res90', 'atr', 'atr_diff', 'atr_ma14', 'rsi', 'rsi_diff', 'rsi_ma14', 'trend_up', 'trend_up3', 'trend_up14', 'trend_up30', 'cs_ss', 'cs_ssr', 'cs_hm', 'cs_hmr', 'cs_brh', 'cs_buh', 'cs_ebu', 'cs_ebr', 'open_1', 'open_2', 'open_3', 'open_4', 'open_5', 'open_6', 'open_7', 'open_8', 'open_9', 'open_10', 'open_11', 'open_12', 'open_13', 'open_14', 'high_1', 'high_2', 'high_3', 'high_4', 'high_5', 'high_6', 'high_7', 'high_8', 'high_9', 'high_10', 'high_11', 'high_12', 'high_13', 'high_14', 'low_1', 'low_2', 'low_3', 'low_4', 'low_5', 'low_6', 'low_7', 'low_8', 'low_9', 'low_10', 'low_11', 'low_12', 'low_13', 'low_14', 'close_1', 'close_2', 'close_3', 'close_4', 'close_5', 'close_6', 'close_7', 'close_8', 'close_9', 'close_10', 'close_11', 'close_12', 'close_13', 'close_14', 'number_of_trades_1', 'number_of_trades_2', 'number_of_trades_3', 'number_of_trades_4', 'number_of_trades_5', 'number_of_trades_6', 'number_of_trades_7', 'number_of_trades_8', 'number_of_trades_9', 'number_of_trades_10', 'number_of_trades_11', 'number_of_trades_12', 'number_of_trades_13', 'number_of_trades_14', 'volume_1', 'volume_2', 'volume_3', 'volume_4', 'volume_5', 'volume_6', 'volume_7', 'volume_8', 'volume_9', 'volume_10', 'volume_11', 'volume_12', 'volume_13', 'volume_14', 'quote_asset_volume_1', 'quote_asset_volume_2', 'quote_asset_volume_3', 'quote_asset_volume_4', 'quote_asset_volume_5', 'quote_asset_volume_6', 'quote_asset_volume_7', 'quote_asset_volume_8', 'quote_asset_volume_9', 'quote_asset_volume_10', 'quote_asset_volume_11', 'quote_asset_volume_12', 'quote_asset_volume_13', 'quote_asset_volume_14', 'taker_buy_base_asset_volume_1', 'taker_buy_base_asset_volume_2', 'taker_buy_base_asset_volume_3', 'taker_buy_base_asset_volume_4', 'taker_buy_base_asset_volume_5', 'taker_buy_base_asset_volume_6', 'taker_buy_base_asset_volume_7', 'taker_buy_base_asset_volume_8', 'taker_buy_base_asset_volume_9', 'taker_buy_base_asset_volume_10', 'taker_buy_base_asset_volume_11', 'taker_buy_base_asset_volume_12', 'taker_buy_base_asset_volume_13', 'taker_buy_base_asset_volume_14', 'taker_buy_quote_asset_volume_1', 'taker_buy_quote_asset_volume_2', 'taker_buy_quote_asset_volume_3', 'taker_buy_quote_asset_volume_4', 'taker_buy_quote_asset_volume_5', 'taker_buy_quote_asset_volume_6', 'taker_buy_quote_asset_volume_7', 'taker_buy_quote_asset_volume_8', 'taker_buy_quote_asset_volume_9', 'taker_buy_quote_asset_volume_10', 'taker_buy_quote_asset_volume_11', 'taker_buy_quote_asset_volume_12', 'taker_buy_quote_asset_volume_13', 'taker_buy_quote_asset_volume_14', 'ma14_1', 'ma14_2', 'ma14_3', 'ma14_4', 'ma14_5', 'ma14_6', 'ma14_7', 'ma14_8', 'ma14_9', 'ma14_10', 'ma14_11', 'ma14_12', 'ma14_13', 'ma14_14', 'ma30_1', 'ma30_2', 'ma30_3', 'ma30_4', 'ma30_5', 'ma30_6', 'ma30_7', 'ma30_8', 'ma30_9', 'ma30_10', 'ma30_11', 'ma30_12', 'ma30_13', 'ma30_14', 'ma90_1', 'ma90_2', 'ma90_3', 'ma90_4', 'ma90_5', 'ma90_6', 'ma90_7', 'ma90_8', 'ma90_9', 'ma90_10', 'ma90_11', 'ma90_12', 'ma90_13', 'ma90_14', 'sup14_1', 'sup14_2', 'sup14_3', 'sup14_4', 'sup14_5', 'sup14_6', 'sup14_7', 'sup14_8', 'sup14_9', 'sup14_10', 'sup14_11', 'sup14_12', 'sup14_13', 'sup14_14', 'sup30_1', 'sup30_2', 'sup30_3', 'sup30_4', 'sup30_5', 'sup30_6', 'sup30_7', 'sup30_8', 'sup30_9', 'sup30_10', 'sup30_11', 'sup30_12', 'sup30_13', 'sup30_14', 'sup90_1', 'sup90_2', 'sup90_3', 'sup90_4', 'sup90_5', 'sup90_6', 'sup90_7', 'sup90_8', 'sup90_9', 'sup90_10', 'sup90_11', 'sup90_12', 'sup90_13', 'sup90_14', 'res14_1', 'res14_2', 'res14_3', 'res14_4', 'res14_5', 'res14_6', 'res14_7', 'res14_8', 'res14_9', 'res14_10', 'res14_11', 'res14_12', 'res14_13', 'res14_14', 'res30_1', 'res30_2', 'res30_3', 'res30_4', 'res30_5', 'res30_6', 'res30_7', 'res30_8', 'res30_9', 'res30_10', 'res30_11', 'res30_12', 'res30_13', 'res30_14', 'res90_1', 'res90_2', 'res90_3', 'res90_4', 'res90_5', 'res90_6', 'res90_7', 'res90_8', 'res90_9', 'res90_10', 'res90_11', 'res90_12', 'res90_13', 'res90_14', 'atr_1', 'atr_2', 'atr_3', 'atr_4', 'atr_5', 'atr_6', 'atr_7', 'atr_8', 'atr_9', 'atr_10', 'atr_11', 'atr_12', 'atr_13', 'atr_14', 'atr_diff_1', 'atr_diff_2', 'atr_diff_3', 'atr_diff_4', 'atr_diff_5', 'atr_diff_6', 'atr_diff_7', 'atr_diff_8', 'atr_diff_9', 'atr_diff_10', 'atr_diff_11', 'atr_diff_12', 'atr_diff_13', 'atr_diff_14', 'atr_ma14_1', 'atr_ma14_2', 'atr_ma14_3', 'atr_ma14_4', 'atr_ma14_5', 'atr_ma14_6', 'atr_ma14_7', 'atr_ma14_8', 'atr_ma14_9', 'atr_ma14_10', 'atr_ma14_11', 'atr_ma14_12', 'atr_ma14_13', 'atr_ma14_14', 'rsi_1', 'rsi_2', 'rsi_3', 'rsi_4', 'rsi_5', 'rsi_6', 'rsi_7', 'rsi_8', 'rsi_9', 'rsi_10', 'rsi_11', 'rsi_12', 'rsi_13', 'rsi_14', 'rsi_diff_1', 'rsi_diff_2', 'rsi_diff_3', 'rsi_diff_4', 'rsi_diff_5', 'rsi_diff_6', 'rsi_diff_7', 'rsi_diff_8', 'rsi_diff_9', 'rsi_diff_10', 'rsi_diff_11', 'rsi_diff_12', 'rsi_diff_13', 'rsi_diff_14', 'rsi_ma14_1', 'rsi_ma14_2', 'rsi_ma14_3', 'rsi_ma14_4', 'rsi_ma14_5', 'rsi_ma14_6', 'rsi_ma14_7', 'rsi_ma14_8', 'rsi_ma14_9', 'rsi_ma14_10', 'rsi_ma14_11', 'rsi_ma14_12', 'rsi_ma14_13', 'rsi_ma14_14', 'trend_up_1', 'trend_up_2', 'trend_up_3', 'trend_up_4', 'trend_up_5', 'trend_up_6', 'trend_up_7', 'trend_up_8', 'trend_up_9', 'trend_up_10', 'trend_up_11', 'trend_up_12', 'trend_up_13', 'trend_up_14', 'trend_up3_1', 'trend_up3_2', 'trend_up3_3', 'trend_up3_4', 'trend_up3_5', 'trend_up3_6', 'trend_up3_7', 'trend_up3_8', 'trend_up3_9', 'trend_up3_10', 'trend_up3_11', 'trend_up3_12', 'trend_up3_13', 'trend_up3_14', 'trend_up14_1', 'trend_up14_2', 'trend_up14_3', 'trend_up14_4', 'trend_up14_5', 'trend_up14_6', 'trend_up14_7', 'trend_up14_8', 'trend_up14_9', 'trend_up14_10', 'trend_up14_11', 'trend_up14_12', 'trend_up14_13', 'trend_up14_14', 'trend_up30_1', 'trend_up30_2', 'trend_up30_3', 'trend_up30_4', 'trend_up30_5', 'trend_up30_6', 'trend_up30_7', 'trend_up30_8', 'trend_up30_9', 'trend_up30_10', 'trend_up30_11', 'trend_up30_12', 'trend_up30_13', 'trend_up30_14', 'cs_ss_1', 'cs_ss_2', 'cs_ss_3', 'cs_ss_4', 'cs_ss_5', 'cs_ss_6', 'cs_ss_7', 'cs_ss_8', 'cs_ss_9', 'cs_ss_10', 'cs_ss_11', 'cs_ss_12', 'cs_ss_13', 'cs_ss_14', 'cs_ssr_1', 'cs_ssr_2', 'cs_ssr_3', 'cs_ssr_4', 'cs_ssr_5', 'cs_ssr_6', 'cs_ssr_7', 'cs_ssr_8', 'cs_ssr_9', 'cs_ssr_10', 'cs_ssr_11', 'cs_ssr_12', 'cs_ssr_13', 'cs_ssr_14', 'cs_hm_1', 'cs_hm_2', 'cs_hm_3', 'cs_hm_4', 'cs_hm_5', 'cs_hm_6', 'cs_hm_7', 'cs_hm_8', 'cs_hm_9', 'cs_hm_10', 'cs_hm_11', 'cs_hm_12', 'cs_hm_13', 'cs_hm_14', 'cs_hmr_1', 'cs_hmr_2', 'cs_hmr_3', 'cs_hmr_4', 'cs_hmr_5', 'cs_hmr_6', 'cs_hmr_7', 'cs_hmr_8', 'cs_hmr_9', 'cs_hmr_10', 'cs_hmr_11', 'cs_hmr_12', 'cs_hmr_13', 'cs_hmr_14', 'cs_brh_1', 'cs_brh_2', 'cs_brh_3', 'cs_brh_4', 'cs_brh_5', 'cs_brh_6', 'cs_brh_7', 'cs_brh_8', 'cs_brh_9', 'cs_brh_10', 'cs_brh_11', 'cs_brh_12', 'cs_brh_13', 'cs_brh_14', 'cs_buh_1', 'cs_buh_2', 'cs_buh_3', 'cs_buh_4', 'cs_buh_5', 'cs_buh_6', 'cs_buh_7', 'cs_buh_8', 'cs_buh_9', 'cs_buh_10', 'cs_buh_11', 'cs_buh_12', 'cs_buh_13', 'cs_buh_14', 'cs_ebu_1', 'cs_ebu_2', 'cs_ebu_3', 'cs_ebu_4', 'cs_ebu_5', 'cs_ebu_6', 'cs_ebu_7', 'cs_ebu_8', 'cs_ebu_9', 'cs_ebu_10', 'cs_ebu_11', 'cs_ebu_12', 'cs_ebu_13', 'cs_ebu_14', 'cs_ebr_1', 'cs_ebr_2', 'cs_ebr_3', 'cs_ebr_4', 'cs_ebr_5', 'cs_ebr_6', 'cs_ebr_7', 'cs_ebr_8', 'cs_ebr_9', 'cs_ebr_10', 'cs_ebr_11', 'cs_ebr_12', 'cs_ebr_13', 'cs_ebr_14']
    elif lookback_days == 3:
        return ['open', 'high', 'low', 'close', 'dow', 'tod', 'number_of_trades', 'volume', 'quote_asset_volume', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ma14', 'ma30', 'ma90', 'sup14', 'sup30', 'sup90', 'res14', 'res30', 'res90', 'atr', 'atr_diff', 'atr_ma14', 'rsi', 'rsi_diff', 'rsi_ma14', 'trend_up', 'trend_up3', 'trend_up14', 'trend_up30', 'cs_ss', 'cs_ssr', 'cs_hm', 'cs_hmr', 'cs_brh', 'cs_buh', 'cs_ebu', 'cs_ebr', 'open_1', 'open_2', 'open_3', 'high_1', 'high_2', 'high_3', 'low_1', 'low_2', 'low_3', 'close_1', 'close_2', 'close_3', 'number_of_trades_1', 'number_of_trades_2', 'number_of_trades_3', 'volume_1', 'volume_2', 'volume_3', 'quote_asset_volume_1', 'quote_asset_volume_2', 'quote_asset_volume_3', 'taker_buy_base_asset_volume_1', 'taker_buy_base_asset_volume_2', 'taker_buy_base_asset_volume_3', 'taker_buy_quote_asset_volume_1', 'taker_buy_quote_asset_volume_2', 'taker_buy_quote_asset_volume_3', 'ma14_1', 'ma14_2', 'ma14_3', 'ma30_1', 'ma30_2', 'ma30_3', 'ma90_1', 'ma90_2', 'ma90_3', 'sup14_1', 'sup14_2', 'sup14_3', 'sup30_1', 'sup30_2', 'sup30_3', 'sup90_1', 'sup90_2', 'sup90_3', 'res14_1', 'res14_2', 'res14_3', 'res30_1', 'res30_2', 'res30_3', 'res90_1', 'res90_2', 'res90_3', 'atr_1', 'atr_2', 'atr_3', 'atr_diff_1', 'atr_diff_2', 'atr_diff_3', 'atr_ma14_1', 'atr_ma14_2', 'atr_ma14_3', 'rsi_1', 'rsi_2', 'rsi_3', 'rsi_diff_1', 'rsi_diff_2', 'rsi_diff_3', 'rsi_ma14_1', 'rsi_ma14_2', 'rsi_ma14_3', 'trend_up_1', 'trend_up_2', 'trend_up_3', 'trend_up3_1', 'trend_up3_2', 'trend_up3_3', 'trend_up14_1', 'trend_up14_2', 'trend_up14_3', 'trend_up30_1', 'trend_up30_2', 'trend_up30_3', 'cs_ss_1', 'cs_ss_2', 'cs_ss_3', 'cs_ssr_1', 'cs_ssr_2', 'cs_ssr_3', 'cs_hm_1', 'cs_hm_2', 'cs_hm_3', 'cs_hmr_1', 'cs_hmr_2', 'cs_hmr_3', 'cs_brh_1', 'cs_brh_2', 'cs_brh_3', 'cs_buh_1', 'cs_buh_2', 'cs_buh_3', 'cs_ebu_1', 'cs_ebu_2', 'cs_ebu_3', 'cs_ebr_1', 'cs_ebr_2', 'cs_ebr_3']
    else:
        return ['open', 'high', 'low', 'close', 'dow', 'tod', 'number_of_trades', 'volume', 'quote_asset_volume', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ma14', 'ma30', 'ma90', 'sup14', 'sup30', 'sup90', 'res14', 'res30', 'res90', 'atr', 'atr_diff', 'atr_ma14', 'rsi', 'rsi_diff', 'rsi_ma14', 'trend_up', 'trend_up3', 'trend_up14', 'trend_up30', 'cs_ss', 'cs_ssr', 'cs_hm', 'cs_hmr', 'cs_brh', 'cs_buh', 'cs_ebu', 'cs_ebr']

def get_target_stoploss(df, threshold_ratio=(0.04,0.02), use_atr=True, atr_ratio=(2,1), reverse=False):
    if not reverse:
        if use_atr:
            stop_losses = df.low-(df.atr*atr_ratio[1])
            targets = df.close+(df.atr*atr_ratio[0])
        else:
            stop_losses = df.close-df.close*threshold_ratio[1]
            targets = df.close+df.close*threshold_ratio[0]
    else:
        if use_atr:
            stop_losses = df.high+(df.atr*atr_ratio[1])
            targets = df.close-(df.atr*atr_ratio[0])
        else:
            stop_losses = df.close+df.close*threshold_ratio[1]
            targets = df.close-df.close*threshold_ratio[0]

    return targets, stop_losses

def load_model(path, device):
    pyt_device = torch.device(device)
    checkpoint = torch.load(path, map_location=pyt_device)
    net = checkpoint['net']
    scaler = checkpoint.get('scaler', None)
    return net, scaler

def predict(model, X, y=None, device='cpu', silent=False):
    pyt_device = torch.device(device)
    if y==None:
        y=pd.DataFrame(np.zeros([len(X),1]))

    if 'cuda' in device:
        # Since it doesn't all fit on the GPU, we'll use a dataloader
        batch_size = 2000
        predictDataset = Dataset(X, y)
        predictLoader = torch.utils.data.DataLoader(dataset=predictDataset,
                                                  batch_size=batch_size,
                                                  shuffle=False,
                                                  num_workers=5,
                                                  pin_memory=True
                                                 )
        num_elements = len(predictLoader.dataset)
        num_outputs = len(y.columns)
        num_batches = len(predictLoader)
        predictions = torch.zeros(num_elements, num_outputs)
        for i, (inputs, _) in enumerate(predictLoader):
            inputs = to_device(inputs, pyt_device)
            start = i*batch_size
            end = start + batch_size
            if i == num_batches - 1:
                end = num_elements
            pred = torch.round(torch.sigmoid(model(inputs)))
            predictions[start:end] = pred.detach().cpu()
        nn_results = predictions.numpy()
    else:
        if type(X) == np.ndarray:
            X_tensor = torch.from_numpy(X).float()
        else:
            X_tensor = torch.from_numpy(X.to_numpy()).float()
        nn_results = torch.round(torch.sigmoid(model(X_tensor))).detach().numpy()

    return nn_results

def make_decision(x_data, extra_data, info_dict):
    x_data = x_data.reset_index(drop=True)
    
    model, scaler = load_model(info_dict['model_filepath'], device=info_dict['model_device'])
    X = scaler.transform(x_data.copy())
    pred = predict(model, X, device=info_dict['model_device'], silent=True)
    
    
    use_atr = info_dict['model_use_atr']
    atr_ratio = info_dict['model_ratio']
    threshold_ratio = info_dict['model_ratio']
    reverse = info_dict['model_reverse']
    targets, stop_losses = get_target_stoploss(x_data, use_atr=use_atr, atr_ratio=atr_ratio, threshold_ratio=threshold_ratio, reverse=reverse)
    #close_prices = x_data['close'].to_numpy()
    low_prices = x_data['low'].to_numpy()
    high_prices = x_data['high'].to_numpy()

    # Next Action:
    # 1 = buy (default)
    # -1 = sell
    next_action = info_dict.get('next_action',1)
    target = info_dict.get('target',-1)
    stoploss = info_dict.get('stoploss',-1)
    
    # Decisions:
    # 1 = buy
    # 0 = hold (default)
    # -1 = sell
    decision = pd.Series(0, index=x_data.index)
    execution_price = pd.Series(0.0, index=x_data.index)

    i = 0
    while True:
        if i>=len(x_data):
            break
        if next_action == 1:
            # Find next buy opportunity
            try:
                next_buy_idx = np.where(pred[i:]==1)[0][0] + i
                target = targets.iloc[next_buy_idx]
                stoploss = stop_losses.iloc[next_buy_idx]
                decision.at[next_buy_idx] = 1
                execution_price.at[next_buy_idx] = x_data.loc[next_buy_idx, 'close']
                i = next_buy_idx+1
                next_action = -1
            except:
                # No more buy opportunties
                break
        else:
            # Find next sell opportunity
            try:
                if not reverse:
                    next_sell_idx = np.where((high_prices[i:]>=target) | (low_prices[i:]<=stoploss))[0][0] + i
                else:
                    next_sell_idx = np.where((low_prices[i:]<=target) | (high_prices[i:]>=stoploss))[0][0] + i
                if x_data.loc[next_sell_idx, 'low'] <= target <= x_data.loc[next_sell_idx, 'high']:
                    execution_price.at[next_sell_idx] = target
                else:
                    execution_price.at[next_sell_idx] = stoploss
                decision.at[next_sell_idx] = -1
                i = next_sell_idx+1
                next_action = 1
            except:
                # No more sell opportunties
                break

    info_dict['next_action'] = next_action
    info_dict['target'] = target
    info_dict['stoploss'] = stoploss

    return decision, execution_price
