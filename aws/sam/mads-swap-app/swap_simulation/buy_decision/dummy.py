# dummy

def columns():
    return ['open', 'high', 'low', 'close']

def make_decision(x_data = [2,3,1,2.1]):
    # return true if buy
    # open / high / low / close
    # if close is higher than open, buy!
    return (x_data[:,3] > (x_data[:,0]*1.005)).reshape(-1,)
