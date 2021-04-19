import numpy as np
from sklearn.utils import shuffle # load training data
from sklearn.model_selection import train_test_split
training_data = np.load('data/training_data.npy')
prices = np.load('data/prices.npy') # print the first 4 samples
print('The first 4 samples are:\n ', training_data[:4])
print('The first 4 prices are:\n ', prices[:4]) # shuffle
training_data, prices = shuffle(training_data, prices, random_state=0)

X_train, X_test, y_train, y_test = train_test_split(training_data, prices, test_size=0.1, random_state=42)


def normalize_data(train_data, test_data, type='minmax'):
    if type == 'standard':
        scaler = preprocessing.StandardScaler()
    elif type == 'minmax':
        scaler = preprocessing.MinMaxScaler()
    else:
        return train_data, test_data
    scaler.fit(train_data)
    scaled_x_train = scaler.transform(train_data)
    scaled_x_test = scaler.transform(test_data)
    return scaled_x_train, scaled_x_test


import sys
from sklearn.model_selection import KFold

def normalize_and_train(training_data, prices):

    training_data, prices = shuffle(training_data, prices, random_state=0)
    X_train, X_test, y_train, y_test = train_test_split(training_data, prices, test_size=0.1, random_state=42)

    minimum = sys.maxsize
    for norm in ['minmax', 'standard', None]:
        X_train_norm, X_test_norm = normalize(X_train, X_test, norm)

        linear_regression_model = LinearRegression()
        kf = KFold(n_splits=3, shuffle=True)
        cv = cross_validate(linear_regression_model, X_train_norm, y_train, cv=kf, scoring=('neg_mean_absolute_error', 'neg_mean_squared_error'))

        print(norm, cv['test_neg_mean_squared_error'], cv['test_neg_mean_absolute_error'])

        if 0 - cv['test_neg_mean_squared_error'].mean() < minimum:
            minimum = 0-cv['test_neg_mean_squared_error'].mean()
            best_norm = norm

    print(best_norm)

min_global = sys.maxsize
for i in [0.1,1,10,100]:
    linear_regression_model = Ridge(alpha=i)

    minimum = sys.maxsize
    for norm in ['minmax', 'standard', None]:
        X_train_norm, X_test_norm = normalize_data(X_train, X_test, norm)
        kf = KFold(n_splits=3, shuffle=True)
        cv = cross_validate(linear_regression_model, X_train_norm, y_train, cv=kf, scoring=('neg_mean_absolute_error', 'neg_mean_squared_error'))


        if 0-cv['test_neg_mean_squared_error'].mean() < minimum:
            minimum = 0-cv['test_neg_mean_squared_error'].mean()
            best_norm = norm

    print("alpha=",i ,best_norm, minimum)

    if minimum < min_global:
        min_global = minimum
        best_alpha = i
        best_norm_global = best_norm

print(best_alpha, min_global, best_norm)