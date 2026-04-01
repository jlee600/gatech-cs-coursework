import numpy as np
import pandas as pd

# Read in the CSV file
# Returns:
#   X: first column is 1s, the rest are from the spreadsheet
#   y: The last column from the spreadsheet
#   labels: The list of headers for the columns of X from the spreadsheet
def read_csv_data(infilename):
    df = pd.read_csv(infilename, index_col=0)
    n, d = df.values.shape
    d = d - 1  # The price column doesn't count
    X = df.values[:, :-1]
    labels = df.columns[:-1]
    y = df.values[:, -1]
    X = np.hstack([np.ones((n, 1)), X])
    return X, y, labels

# Returns a vector of weights
def matrix_inversion_fit(X, y):
    ## Your code here
    # B = (X^T * X)^-1 * X^T * y
    xt = X.T
    var1 = np.linalg.inv(np.dot(xt, X))
    var2 = np.dot(xt, y)
    b = np.dot(var1, var2)
    return b

# Returns a vector of weights
def gradient_descent_fit(X, y):
    # Standardize the data (except for the first column!)
    # Get the mean and standard deviation for each column
    ## Your code here

    # Iteratively use gradient descent to get
    # a good estimate of the parameters
    # Start with all zeros as your first guess
    # Stop when the change in the parameters gets very small
    # Experiment to find a good learning rate
    # You should expect a few hundred iterations
    iter_count = 0

    ## Your code here
    n, d = X.shape
    b = np.zeros(d)
    b2 = np.zeros(d)

    m = np.mean(X[:, 1:], axis=0)
    s = np.std(X[:, 1:], axis=0)

    x = np.copy(X)
    x[:, 1:] = (X[:, 1:] - m) / s

    while iter_count < 10000:
        dist = x.dot(b2) - y
        gradient = (2/n) * x.T.dot(dist)
        
        tmep = -0.1 * gradient 
        b2 = b2 + tmep
        iter_count += 1

        if np.linalg.norm(tmep) < 1e-8:
            break

    print(f"Took {iter_count} iterations to converge")

    ## Your code here
    b[1:] = b2[1:] / s
    b[0] = b2[0] - np.sum(b2[1:] * m / s)
    
    return b

# Make it pretty
def format_prediction(B, labels):
    str = f"predicted price = ${B[0]:,.2f} + "
    d = len(labels)
    for i in range(d):
        b = B[i + 1]
        label = labels[i]
        str += f"(${b:,.2f} x {label})"
        if i < d - 1:
            str += " + "
    return str

# Return the R2 score for coefficients B
# Given inputs X and outputs y
def score(b, X, y):
    ## Your code here
    total = np.sum((y - np.mean(y)) ** 2)
    s = np.sum((y - X.dot(b)) ** 2)
    
    return 1 - (s / total)
