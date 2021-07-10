# dummy
import numpy as np

def columns():
    return ['open', 'high', 'low', 'close']

def stop_loss_target_range(x_data = [2,3,1,2.1]):
    # return tuple of (stop-loss, sell target)
    return np.array([x_data[:, 0] * 0.95, x_data[:, 0] * 1.05]).T