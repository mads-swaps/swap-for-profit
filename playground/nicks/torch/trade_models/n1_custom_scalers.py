from sklearn.preprocessing import StandardScaler
import re

class CustomScaler1():
    stdcols = ('number_of_trades','volume','quote_asset_volume',
               'taker_buy_base_asset_volume','taker_buy_quote_asset_volume',
               )
    
    def __init__(self):
        self.standard_scaler = StandardScaler()
        self.tostd = []
        self.is_fit = False
        
    def fit(self, X):
        for c in self.stdcols:
            for v in X.columns:
                if v.startswith(c):
                    self.tostd.append(v)
                
        if len(self.tostd) > 0:
            self.standard_scaler.fit(X[self.tostd])
            
        self.is_fit = True
        return self
        
    def transform(self, X_in):
        if self.is_fit == True:
            X = X_in.copy()
            open_price = X['open'].copy()
            stddev = (((X['close'] - X['open'])**2 + \
                       (X['high'] - X['open'])**2 + \
                       (X['low'] - X['open'])**2) / 3)**0.5
            stddev = stddev.apply(lambda x: 1 if x==0 else x)
            
            rsi_values = X['rsi'].copy()
            atr_values = X['atr'].copy()
            atr_values = atr_values.apply(lambda x: 1 if x==0 else x)
            
            for c in X.columns:
                if c in ['open','high','low','close'] or \
                   re.match('open_[0-9]+', c) or \
                   re.match('high_[0-9]+', c) or \
                   re.match('low_[0-9]+', c) or \
                   re.match('close_[0-9]+', c) or \
                   re.match('sup[0-9]+', c) or \
                   re.match('res[0-9]+', c) or \
                   re.match('ma[0-9]+', c):
                    X[c] = (X[c]-open_price)/stddev
                elif c.startswith('atr_diff'):
                    X[c] = X[c]/atr_values
                elif re.match('atr$|atr_[0-9]+|atr_ma[0-9]+',c):
                    X[c] = X[c]-atr_values/atr_values
                elif c.startswith('rsi_diff'):
                    X[c] = X[c]/rsi_values
                elif re.match('rsi$|rsi_[0-9]+|rsi_ma[0-9]+',c):
                    X[c] = (X[c]-50)/20 # thus the 30/70 thresholds will become -1/1
            
            if 'dow' in X.columns:
                X['dow'] = X['dow'] / 6
                
            if len(self.tostd) > 0:
                X[self.tostd] = self.standard_scaler.transform(X[self.tostd])
            return X
        else:
            raise Exception('CustomScaler not yet fit')
            
    def fit_transform(self, X_in, y=None):
        self.fit(X_in)
        y=self.transform(X_in)
        return y
