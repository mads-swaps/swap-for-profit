import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier

from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

from sklearn.model_selection import GridSearchCV

def train_test_split(X, y, train_idx=None, test_idx=None):
    X_train = X.loc[train_idx]
    y_train = y.loc[train_idx]
    X_test = X.loc[test_idx]
    y_test = y.loc[test_idx]
    return (X_train, y_train, X_test, y_test)

def load_data(suffix=None, split=False):
    if suffix==None:
        suffix='DEFAULT'

    X = pd.read_pickle(f'../../data/X_{suffix}.pkl')
    y = pd.read_pickle(f'../../data/y_{suffix}.pkl')

    if split:
        X_train, y_train, X_test, y_test = train_test_split(X, y, X.loc[:'2019'].index, X.loc['2020':].index)
        return X_train, y_train, X_test, y_test
    else:
        return X, y

def perform_grid_search():
    X,y = load_data(suffix='20210715')

    # parameters = {'learning_rate': [0.03, 0.06, 0.1],
    #               'loss': ['deviance', 'exponential'],
    #               'n_estimators': [100, 500, 1000],
    #               'criterion': ['friedman_mse', 'mse', 'mae'],
    #               'max_depth' : [3,4,5],
    #               'random_state': [0],
    #               'max_features' : [None, 'sqrt', 'log2']
    #              }

    parameters = {'learning_rate': [0.001, 0.003, 0.006, 0.01, 0.03, 0.06, 0.1, 0.3, 0.6, 1],
              'loss': ['deviance'],
              'n_estimators': [100],
              'criterion': ['friedman_mse'],
              'max_depth' : [3],
              'random_state': [0],
              'max_features' : [None]
             }

    gbc = GradientBoostingClassifier()
    clf = GridSearchCV(gbc, parameters, n_jobs=-1, verbose=4, scoring='precision').fit(X, y)

    pd.DataFrame(clf.cv_results_).to_csv('grid_search_output.csv')


if __name__ == '__main__':
    perform_grid_search()
