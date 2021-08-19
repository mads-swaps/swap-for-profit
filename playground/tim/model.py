import torch
import torch.nn as nn

class NNModel(nn.Module):
    def __init__(self, inputSize, outputSize, hiddenSize, activate=None):
        super().__init__()
        self.activate = nn.Sigmoid() if activate == "Sigmoid" else nn.Tanh() if activate == "Tanh" else nn.ReLU()
        self.layer1 = nn.Linear(inputSize, hiddenSize)
        self.layer2 = nn.Linear(hiddenSize, outputSize)

    def forward(self, X):
        hidden = self.activate(self.layer1(X))
        return self.layer2(hidden)


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

    
    
    
    
    
    
    
    
class CNNModel(nn.Module):
    def __init__(self, inputSize, outputSize, lookback_count, model_definition):
        super().__init__()

        network = []
        
        self.num_features = inputSize // lookback_count
        self.lookback_count = lookback_count

        self.conv1d_1 = nn.Conv1d(self.num_features, 80, 4)
        self.relu_1 = nn.ReLU()
        self.conv1d_2 = nn.Conv1d(80, 40, 4, stride=2)
        self.relu_2 = nn.ReLU()
        p = 360 + inputSize
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

        network.append(nn.Linear(in_features=p, out_features=outputSize))
        #network.append(nn.ReLU())

        self.net = nn.Sequential(*network)

    def forward(self, X):
        X2 = X.clone()
        X2 = torch.reshape(X2, (X.shape[0], self.num_features, self.lookback_count))
        X2 = self.conv1d_1(X2)
        X2 = self.relu_1(X2)
        X2 = self.conv1d_2(X2)
        X2 = self.relu_2(X2)
        X2 = torch.reshape(X2, (X2.shape[0],-1))
        X = torch.cat((X,X2),1)
        return self.net(X)
