from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split

def fit_model(model, X, y, params=None):
    if params!=None:
        model.set_params(**params)
    model.fit(X,y)

def predict_y(model, X):
    return model.predict(X)
    
def score_oob(model):
    modelself.

def data_frame_subset(X, y, n_subset):
    row_selected = list(np.random.randint(0, df.shape[0],  num_rows))
    X_sub_set = X[row_selected, :]
    y_sub_set = y[row_selected]
    return X_sub_set, y_sub_set

def pipeline(model, X, y, n_subset, params=None):
    _x, _y = data_frame_subset(X,y,n_subset)  
    X_train, X_test, y_train, y_test = train_test_split(_x,_y)
    fit_model(model, X_train, y_train, params)
    mse_array = cross_val_score(model, X_test, y_test, cv=5, scoring='mean_squared_erroe')
    r2_array = cross_val_score(model, X_test, y_test, cv=5, scoring='r2')
    return np.mean(np.abs(mse_array)), np.mean(np.abs(r2_array))
