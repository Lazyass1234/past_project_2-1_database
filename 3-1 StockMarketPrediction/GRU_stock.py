import numpy as np
import random
import pandas as pd
from pylab import mpl, plt
plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

from pandas import datetime
import math, time
import itertools
import datetime
from operator import itemgetter
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from math import sqrt
import torch
import torch.nn as nn
from torch.autograd import Variable

metadata = pd.read_csv("metadata.csv").set_index('Unnamed: 0')  #days 814, companies 845
metadata.index.names = ['dates']
metadata.columns.names = ['tickers']
ticker_list = list(metadata)

# Normalization first
############################################
scaler = MinMaxScaler(feature_range=(-1, 1))
for ticker in ticker_list:
    metadata[ticker] = scaler.fit_transform(metadata[ticker].values.reshape(-1, 1))

# function to create train, test data given stock data and sequence length
def load_data(stock, look_back):
    data_raw = stock.values # convert to numpy array
    data = []
    
    # create all possible sequences of length look_back
    for index in range(len(data_raw) - look_back): 
        data.append(data_raw[index: index + look_back])
    
    data = np.array(data);
    test_set_size = int(np.round(0.2*data.shape[0]));
    train_set_size = data.shape[0] - (test_set_size);
    
    x_train = data[:train_set_size,:-1,:]
    y_train = data[:train_set_size,-1,:]
    
    x_test = data[train_set_size:,:-1]
    y_test = data[train_set_size:,-1,:]
    
    return [x_train, y_train, x_test, y_test]

look_back = 24 # choose sequence length

RMSE_train = []
RMSE_test = []
for ticker in ticker_list:
    x_train, y_train, x_test, y_test = load_data(pd.DataFrame(metadata[ticker]), look_back)
    print('x_train.shape = ',x_train.shape)
    print('y_train.shape = ',y_train.shape)
    print('x_test.shape = ',x_test.shape)
    print('y_test.shape = ',y_test.shape)
    
    # make training and test sets in torch
    x_train = torch.from_numpy(x_train).type(torch.Tensor)
    x_test = torch.from_numpy(x_test).type(torch.Tensor)
    y_train = torch.from_numpy(y_train).type(torch.Tensor)
    y_test = torch.from_numpy(y_test).type(torch.Tensor)
    
    print(y_train.size(),x_train.size())
    
    # Build model
    #####################
    input_dim = 1
    hidden_dim = 32
    num_layers = 2 
    output_dim = 1
    
    class GRUNet(nn.Module):
        def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
            super(GRUNet, self).__init__()
            self.hidden_dim = hidden_dim
            self.num_layers = num_layers
            
            self.gru = nn.GRU(input_dim, hidden_dim, num_layers, batch_first=True)
            self.fc = nn.Linear(hidden_dim, output_dim)
    
        def forward(self, x):
            h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
            out, (hn) = self.gru(x, (h0.detach()))
            out = self.fc(out[:, -1, :]) 
            return out
    
    model = GRUNet(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)
    
    loss_fn = torch.nn.MSELoss()
    
    optimiser = torch.optim.Adam(model.parameters(), lr=0.01)
    print(model)
    print(len(list(model.parameters())))
    for i in range(len(list(model.parameters()))):
        print(list(model.parameters())[i].size())
        
    # Train model
    #####################
    num_epochs = 100
    hist = np.zeros(num_epochs)
    
    # Number of steps to unroll
    seq_dim =look_back-1  
    
    for t in range(num_epochs):
        # Initialise hidden state
        # Don't do this if you want your LSTM to be stateful
        #model.hidden = model.init_hidden()
        
        # Forward pass
        y_train_pred = model(x_train)
    
        loss = loss_fn(y_train_pred, y_train)
        if t % 10 == 0 and t !=0:
            print("Epoch ", t, "MSE: ", loss.item())
        hist[t] = loss.item()
    
        # Zero out gradient, else they will accumulate between epochs
        optimiser.zero_grad()
    
        # Backward pass
        loss.backward()
    
        # Update parameters
        optimiser.step()
        
    #plt.plot(hist, label="Training loss")
    #plt.legend()
    #plt.show()
    
    np.shape(y_train_pred)
    
    # make predictions
    y_test_pred = model(x_test)
    
    # invert predictions
    y_train_pred = scaler.inverse_transform(y_train_pred.detach().numpy())
    y_train = scaler.inverse_transform(y_train.detach().numpy())
    y_test_pred = scaler.inverse_transform(y_test_pred.detach().numpy())
    y_test = scaler.inverse_transform(y_test.detach().numpy())
    
    # calculate root mean squared error
    trainScore = math.sqrt(mean_squared_error(y_train[:,0], y_train_pred[:,0]))
    print('Train Score: %.2f RMSE' % (trainScore))
    testScore = math.sqrt(mean_squared_error(y_test[:,0], y_test_pred[:,0]))
    print('Test Score: %.2f RMSE' % (testScore))
    RMSE_train.append(trainScore)
    RMSE_test.append(testScore)
    
    # Visualising the results
    figure, axes = plt.subplots(figsize=(15, 6))
    axes.xaxis_date()
    
    axes.plot(pd.DataFrame(metadata[ticker])[len(pd.DataFrame(metadata[ticker]))-len(y_test):].index, y_test, color = 'red', label = 'Real Closing Price')
    axes.plot(pd.DataFrame(metadata[ticker])[len(pd.DataFrame(metadata[ticker]))-len(y_test):].index, y_test_pred, color = 'blue', label = 'Predicted Closing Price')
    #axes.xticks(np.arange(0,394,50))
    plt.title('Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.savefig('GRU_pngs//%s_pred.png'%ticker)
    #plt.show()
with open("GRU_RMSE_train.txt", "w") as output:
    output.write(str(RMSE_train))
with open("GRU_RMSE_test.txt", "w") as output:
    output.write(str(RMSE_test))