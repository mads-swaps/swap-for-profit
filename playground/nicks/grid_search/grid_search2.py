import pandas as pd
import numpy as np
import re

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import GridSearchCV, PredefinedSplit

def train_test_split(X, y, train_idx=None, test_idx=None):
    X_train = X.loc[train_idx]
    y_train = y.loc[train_idx]
    X_test = X.loc[test_idx]
    y_test = y.loc[test_idx]
    return (X_train, y_train, X_test, y_test)

def load_split_data(suffix, split=False):
    X = pd.read_pickle(f'../../data/X_{suffix}.pkl')
    y = pd.read_pickle(f'../../data/y_{suffix}.pkl')
    if split:
        X_train, y_train, X_test, y_test = train_test_split(X, y, X.loc['2018':'2020'].index, X.loc['2021':].index)
        return X_train, y_train, X_test, y_test
    else:
        return X, y

def get_columns(X,lookbacks):
    # Drop columns with lookbacks equal to or greater than X
    columns = list(X.columns)
    for c in X.columns:
        if m := re.match(r'^.*_([0-9]+)$', c):
            if int(m[1]) > lookbacks:
                columns.remove(c)
    return columns

def get_cv_train_test_split(X):
    # Returns a single fold with train/test split
    train_indices = np.full((len(X.loc['2018':'2020']),), -1, dtype=int)
    test_indices =  np.full((len(X.loc['2021':]),), 0, dtype=int)
    test_fold = np.append(train_indices, test_indices)
    
    ps = PredefinedSplit(test_fold)
    ps.get_n_splits()
    return ps

def perform_grid_search1():
    X,y = load_split_data('20210806i')
    ps = get_cv_train_test_split(X)
    columns = get_columns(X, 15)

    parameters = {
        #'n_estimators': [100,500,1000],
        'learning_rate': [0.05,0.1,0.5],
        'loss': ['deviance', 'exponential'],
        'criterion': ['friedman_mse', 'mse', 'mae'],
        'max_depth': [2,3,4],
        'max_features': ['sqrt','log2',len(columns)]
    }

    c = GradientBoostingClassifier(random_state=42)
    clf = GridSearchCV(c, parameters, verbose=4, cv=ps, scoring='precision', n_jobs=-1) \
            .fit(X.loc['2018':][columns], y.loc['2018':].buy)

    pd.DataFrame(clf.cv_results_).to_csv('gb_grid_search1.csv')

    
def perform_grid_search2():
    X,y = load_split_data('20210806i')
    ps = get_cv_train_test_split(X)
    columns = get_columns(X, 3)

    parameters = {
        #'n_estimators': [100,500,1000],
        'learning_rate': [0.05,0.1,0.5],
        'loss': ['deviance', 'exponential'],
        'criterion': ['friedman_mse', 'mse', 'mae'],
        'max_depth': [2,3,4],
        'max_features': ['sqrt','log2',len(columns)]
    }

    c = GradientBoostingClassifier(random_state=42)
    clf = GridSearchCV(c, parameters, verbose=4, cv=ps, scoring='precision', n_jobs=-1) \
            .fit(X.loc['2018':][columns], y.loc['2018':].buy)

    pd.DataFrame(clf.cv_results_).to_csv('gb_grid_search2.csv')

if __name__ == '__main__':
    perform_grid_search1()
    perform_grid_search2()
