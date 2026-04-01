"""
Part 4: Cross-validation with scratch KNN
Run: python part4_crossval_scratch.py

This will:
 - load the HAR dataset (expects the "UCI HAR Dataset" folder in current dir)
 - sample a subset to keep runtime manageable
 - run manual k-fold cross-validation using our scratch KNN (from utils.py)
 - search k = 1..20
 - report the best k based on CV
 - retrain with best k and evaluate on held-out test set
"""

import numpy as np
from utils import load_har_dataset, display_confusion_matrix_and_accuracy
from part2_sklearn import KNN_using_sklearn


def cross_validate_knn(X, y, k, n_splits=6, random_state=42):
    """
    Perform manual k-fold cross-validation using scratch KNN.
    Returns mean accuracy across folds.
    """
    np.random.seed(random_state)
    indices = np.arange(len(X))
    np.random.shuffle(indices)

    # Your code goes here
    folds = np.array_split(indices, n_splits)
    results = {}

    for k in range(1, 21):
        accf = []

        for i in range(n_splits):
            temp = []
            for j, fold in enumerate(folds):
                if j != i:
                    temp.append(fold)
            tidx = np.concatenate(temp)

            idx = folds[i]
            xtrain, ytrain = X[tidx], y[tidx]
            pred, acc = KNN_using_sklearn(xtrain, ytrain, X[idx], y[idx], k)
            accf.append(acc)

        results[k] = np.mean(accf)

    return results


def main():
    print("Part 4: Cross-validation with scratch KNN")

    # Your code goes here
    xtrain, ytrain, xtest, ytest = load_har_dataset()
    cv = cross_validate_knn(xtrain, ytrain, k=5, n_splits=6)
    for k, mean_acc in cv.items():
        print(f"k={k:2d}, Mean CV Accuracy={mean_acc*100:.2f}%")

    best = max(cv, key=cv.get)

    pred, acc = KNN_using_sklearn(xtrain, ytrain, xtest, ytest, best)
    print(f"\nBest k from CV: {best} with accuracy={cv[best]*100:.2f}%")

    display_confusion_matrix_and_accuracy(best, ytest, pred)

    # Below are the print functions. Use them as needed.
    # print(f"k={k:2d}, Mean CV Accuracy={mean_acc*100:.2f}%")



if __name__ == "__main__":
    main()