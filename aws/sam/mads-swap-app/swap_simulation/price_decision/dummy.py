# dummy

def columns():
    return ['open', 'high', 'low', 'close']

def stop_loss_target_range(x_data = [2,3,1,2.1]):
    # return tuple of (stop-loss, sell target)
    current_price = x_data[0]
    return (current_price * 0.95, current_price * 1.05)