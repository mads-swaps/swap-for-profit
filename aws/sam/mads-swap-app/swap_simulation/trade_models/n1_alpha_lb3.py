import numpy as np
import pandas as pd
import pickle

def columns():
    return ['open', 'high', 'low', 'close', 'dow', 'tod', 'number_of_trades', 'volume', 'quote_asset_volume', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ma14', 'ma30', 'ma90', 'sup14', 'sup30', 'sup90', 'res14', 'res30', 'res90', 'atr', 'atr_diff', 'atr_ma14', 'rsi', 'rsi_diff', 'rsi_ma14', 'trend_up', 'trend_up3', 'trend_up14', 'trend_up30', 'cs_ss', 'cs_ssr', 'cs_hm', 'cs_hmr', 'cs_brh', 'cs_buh', 'cs_ebu', 'cs_ebr', 'open_1', 'open_2', 'open_3', 'high_1', 'high_2', 'high_3', 'low_1', 'low_2', 'low_3', 'close_1', 'close_2', 'close_3', 'number_of_trades_1', 'number_of_trades_2', 'number_of_trades_3', 'volume_1', 'volume_2', 'volume_3', 'quote_asset_volume_1', 'quote_asset_volume_2', 'quote_asset_volume_3', 'taker_buy_base_asset_volume_1', 'taker_buy_base_asset_volume_2', 'taker_buy_base_asset_volume_3', 'taker_buy_quote_asset_volume_1', 'taker_buy_quote_asset_volume_2', 'taker_buy_quote_asset_volume_3', 'ma14_1', 'ma14_2', 'ma14_3', 'ma30_1', 'ma30_2', 'ma30_3', 'ma90_1', 'ma90_2', 'ma90_3', 'sup14_1', 'sup14_2', 'sup14_3', 'sup30_1', 'sup30_2', 'sup30_3', 'sup90_1', 'sup90_2', 'sup90_3', 'res14_1', 'res14_2', 'res14_3', 'res30_1', 'res30_2', 'res30_3', 'res90_1', 'res90_2', 'res90_3', 'atr_1', 'atr_2', 'atr_3', 'atr_diff_1', 'atr_diff_2', 'atr_diff_3', 'atr_ma14_1', 'atr_ma14_2', 'atr_ma14_3', 'rsi_1', 'rsi_2', 'rsi_3', 'rsi_diff_1', 'rsi_diff_2', 'rsi_diff_3', 'rsi_ma14_1', 'rsi_ma14_2', 'rsi_ma14_3', 'trend_up_1', 'trend_up_2', 'trend_up_3', 'trend_up3_1', 'trend_up3_2', 'trend_up3_3', 'trend_up14_1', 'trend_up14_2', 'trend_up14_3', 'trend_up30_1', 'trend_up30_2', 'trend_up30_3', 'cs_ss_1', 'cs_ss_2', 'cs_ss_3', 'cs_ssr_1', 'cs_ssr_2', 'cs_ssr_3', 'cs_hm_1', 'cs_hm_2', 'cs_hm_3', 'cs_hmr_1', 'cs_hmr_2', 'cs_hmr_3', 'cs_brh_1', 'cs_brh_2', 'cs_brh_3', 'cs_buh_1', 'cs_buh_2', 'cs_buh_3', 'cs_ebu_1', 'cs_ebu_2', 'cs_ebu_3', 'cs_ebr_1', 'cs_ebr_2', 'cs_ebr_3']


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

def make_decision(x_data, extra_data, info_dict):
    x_data = x_data.reset_index(drop=True)
    
    clf = pickle.load(open(info_dict['portfolio']['model_filepath'], 'rb'))
    pred = clf.predict(x_data)
    use_atr = info_dict['portfolio']['model_use_atr']
    atr_ratio = info_dict['portfolio']['model_ratio']
    threshold_ratio = info_dict['portfolio']['model_ratio']
    reverse = info_dict['portfolio']['model_reverse']
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
