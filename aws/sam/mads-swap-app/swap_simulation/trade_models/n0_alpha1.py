import numpy as np
import pandas as pd
import pickle

def columns():
    return ['open', 'high', 'low', 'close', 'rsi_13', 'ma30_8', 'atr_diff_9', 'cs_hm_9', 'rsi_diff_8', 'low_5', 'high_10', 'low_7', 'cs_hm_14', 'open_5', 'cs_ebu', 'rsi_2', 'atr_ma14_1', 'close_4', 'high_2', 'cs_hmr_9', 'rsi_diff_6', 'ma90', 'open_3', 'trend_up14_13', 'tod', 'atr_3', 'trend_up3_1', 'cs_ss_8', 'ma14_12', 'atr_diff_4', 'trend_up30_10', 'trend_up3_11', 'rsi_ma14_5', 'atr_ma14_2', 'rsi_ma14_9', 'close_13', 'close_12', 'trend_up14_2', 'cs_ssr_5', 'rsi_ma14_14', 'ma30_9', 'trend_up14_8', 'trend_up30_5', 'rsi_ma14_7', 'high_11', 'cs_hm_2', 'rsi_diff', 'cs_ss_7', 'cs_ssr_13', 'cs_ebu_6', 'cs_ebu_8', 'cs_brh_13', 'cs_brh_9', 'number_of_trades', 'ma30', 'atr_11', 'rsi_diff_4', 'cs_ebu_4', 'ma90_5', 'high_13', 'ma90_4', 'cs_ss_3', 'cs_hmr_8', 'cs_ebu_2', 'cs_buh_2', 'trend_up_3', 'trend_up30_2', 'rsi_diff_14', 'atr_ma14_10', 'trend_up_12', 'rsi_diff_5', 'rsi_diff_7', 'trend_up_7', 'atr_diff_6', 'cs_buh_1', 'low_10', 'atr_12', 'cs_ss_10', 'atr_10', 'cs_brh_3', 'cs_ssr_11', 'cs_ebr_11', 'trend_up3_12', 'cs_buh_14', 'rsi_ma14_10', 'trend_up3', 'cs_hmr_5', 'cs_brh_1', 'cs_ss_1', 'cs_brh', 'cs_ss', 'close_5', 'high_12', 'atr', 'cs_ebr_13', 'rsi_4', 'cs_hm_1', 'ma90_6', 'open_9', 'cs_ebr', 'ma30_11', 'ma90_7', 'rsi_diff_1', 'cs_hmr_14', 'ma14_1', 'ma90_8', 'cs_ssr', 'cs_hm_5', 'open_2', 'trend_up14_11', 'cs_ssr_14', 'atr_diff_14', 'rsi_6', 'cs_hmr_4', 'close_7', 'low_12', 'cs_ebu_10', 'rsi_diff_11', 'cs_buh_11', 'ma90_1', 'cs_ss_4', 'cs_hmr_12', 'cs_hmr_11', 'trend_up30_11', 'cs_buh_3', 'trend_up3_10', 'high_14', 'trend_up14_1', 'atr_diff_5', 'cs_hm', 'atr_diff_11', 'cs_hm_7', 'trend_up3_8', 'cs_brh_5', 'cs_ssr_9', 'high_6', 'rsi_diff_13', 'ma30_1', 'trend_up3_3', 'trend_up30_12', 'ma30_12', 'high_5', 'cs_hmr_2', 'rsi_7', 'cs_ss_12', 'dow', 'trend_up14_10', 'atr_4', 'open_8', 'atr_diff', 'rsi_ma14_13', 'rsi', 'ma30_4', 'atr_1', 'cs_ebr_5', 'atr_7', 'cs_buh_8', 'cs_ssr_4', 'trend_up14_14', 'cs_hmr', 'cs_buh_6', 'cs_brh_7', 'ma30_10', 'atr_diff_3', 'atr_ma14_14', 'cs_buh_5', 'cs_ss_9', 'cs_ebu_1', 'cs_ebr_9', 'cs_buh_10', 'high_7', 'atr_diff_1', 'atr_ma14_13', 'trend_up_11', 'trend_up3_14', 'open_10', 'close_6', 'trend_up_1', 'atr_2', 'trend_up_5', 'trend_up3_6', 'ma90_14', 'rsi_8', 'high_9', 'rsi_ma14_8', 'atr_ma14', 'atr_diff_8', 'rsi_ma14_12', 'trend_up14_3', 'rsi_11', 'cs_hmr_13', 'ma90_12', 'cs_brh_8', 'ma30_13', 'cs_hm_11', 'cs_brh_2', 'trend_up14_6', 'close_3', 'cs_brh_4', 'trend_up3_9', 'cs_hmr_3', 'trend_up_2', 'cs_hm_4', 'rsi_3', 'trend_up30_8', 'cs_ebu_13', 'trend_up14', 'trend_up3_5', 'atr_ma14_9', 'cs_ebu_11', 'cs_ebu_7', 'rsi_diff_3', 'cs_ebr_1', 'rsi_diff_12', 'cs_buh_4', 'open_14', 'ma90_9', 'atr_diff_12', 'rsi_ma14_4', 'atr_9', 'ma14_2', 'cs_buh', 'ma90_10', 'ma14_8', 'rsi_diff_2', 'ma30_6', 'atr_13', 'trend_up3_4', 'low_4', 'cs_ssr_7', 'cs_ebr_6', 'cs_hmr_6', 'low_11', 'atr_5', 'cs_ss_13', 'atr_ma14_4', 'trend_up3_2', 'cs_hmr_10', 'quote_asset_volume', 'trend_up30_3', 'volume', 'close_10', 'cs_ebu_3', 'ma14_3', 'rsi_ma14_1', 'atr_diff_7', 'ma14_5', 'trend_up_6', 'cs_brh_12', 'high_3', 'cs_ebr_8', 'close_2', 'trend_up14_12', 'cs_hm_8', 'rsi_ma14_2', 'high_4', 'cs_brh_11', 'open_12', 'ma14_10', 'ma14_13', 'low_3', 'cs_hm_6', 'low_2', 'cs_hm_3', 'cs_ssr_6', 'trend_up_10', 'close_11', 'cs_hm_10', 'close_14', 'atr_diff_2', 'taker_buy_base_asset_volume', 'high_8', 'cs_ss_6', 'cs_hm_13', 'trend_up_9', 'cs_ssr_3', 'trend_up30_6', 'close_9', 'atr_ma14_6', 'cs_brh_6', 'trend_up_4', 'open_13', 'trend_up_8', 'trend_up3_7', 'cs_buh_7', 'trend_up14_5', 'trend_up3_13', 'low_9', 'trend_up_14', 'open_6', 'rsi_14', 'trend_up14_7', 'close_8', 'cs_ssr_1', 'high_1', 'rsi_ma14_6', 'cs_ssr_12', 'cs_ssr_2', 'rsi_10', 'atr_6', 'low_14', 'ma14_9', 'ma30_3', 'low_8', 'rsi_ma14_11', 'ma14_7', 'trend_up30_1', 'trend_up14_4', 'rsi_diff_10', 'ma90_13', 'atr_ma14_7', 'cs_ebr_2', 'cs_ebr_14', 'cs_ebu_14', 'ma14', 'cs_ebu_5', 'cs_hm_12', 'ma30_7', 'trend_up30_9', 'cs_buh_13', 'ma30_2', 'ma90_3', 'ma30_14', 'ma14_6', 'cs_ss_11', 'taker_buy_quote_asset_volume', 'atr_ma14_12', 'rsi_ma14_3', 'cs_ebu_12', 'atr_ma14_3', 'open_1', 'ma14_14', 'low_6', 'ma14_4', 'rsi_12', 'open_11', 'trend_up14_9', 'rsi_diff_9', 'cs_ebr_10', 'cs_hmr_7', 'atr_8', 'cs_ebr_12', 'cs_ss_14', 'close_1', 'cs_ss_2', 'rsi_5', 'ma30_5', 'cs_ssr_8', 'trend_up30_7', 'low_1', 'cs_ebr_3', 'atr_diff_13', 'cs_brh_10', 'trend_up30', 'cs_ss_5', 'atr_14', 'low_13', 'cs_hmr_1', 'cs_buh_9', 'trend_up30_13', 'rsi_9', 'trend_up', 'ma90_2', 'atr_diff_10', 'rsi_1', 'ma90_11', 'ma14_11', 'trend_up30_14', 'cs_ebr_4', 'cs_ebr_7', 'cs_buh_12', 'cs_ebu_9', 'open_4', 'open_7', 'atr_ma14_8', 'trend_up30_4', 'atr_ma14_11', 'atr_ma14_5', 'cs_brh_14', 'cs_ssr_10', 'rsi_ma14', 'trend_up_13']


def get_target_stoploss(df, threshold_ratio=(0.04,0.02), use_atr=True, atr_ratio=(2,1)):
    if use_atr:
        low_pip = (df.close-df.low)/df.close
        stop_losses = df.close-df.close*(df.atr*atr_ratio[1] + low_pip)
        targets = df.close+df.close*(df.atr*atr_ratio[0])
    else:
        stop_losses = df2.close-df2.close*threshold_ratio[1]
        targets = df2.close+df2.close*threshold_ratio[0]

    return targets, stop_losses

def make_decision(x_data, extra_data, info_dict):
    # Replace any boolean or object columns as int
    for col in x_data.columns:
        if x_data[col].dtype.kind in ['b','O']:
            x_data[col] = x_data[col].astype(int)
    
    clf = pickle.load(open(info_dict['portfolio']['model_filepath'], 'rb'))
    pred = clf.predict(x_data)
    targets, stop_losses = get_target_stoploss(x_data, use_atr=True, atr_ratio=(20,5))
    close_prices = x_data['close'].to_numpy()

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
                i = next_buy_idx+1
                next_action = -1
            except:
                # No more buy opportunties
                break
        else:
            # Find next sell opportunity
            try:
                next_sell_idx = np.where((close_prices[i:]>=target) | (close_prices[i:]<=stoploss))[0][0] + i
                decision.at[next_sell_idx] = -1
                i = next_sell_idx+1
                next_action = 1
            except:
                # No more sell opportunties
                break

    info_dict['next_action'] = next_action
    info_dict['target'] = target
    info_dict['stoploss'] = stoploss

    return decision
