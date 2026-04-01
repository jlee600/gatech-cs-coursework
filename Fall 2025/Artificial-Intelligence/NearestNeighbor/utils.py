"""
utils.py
Common utilities for the HAR KNN assignments with tie-breaking.
"""

import os
import numpy as np
from typing import Tuple


def load_har_dataset(base_path: str = "UCI HAR Dataset") -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load the HAR dataset from the UCI archive."""
    train_x = os.path.join(base_path, "train", "X_train.txt")
    train_y = os.path.join(base_path, "train", "y_train.txt")
    test_x = os.path.join(base_path, "test", "X_test.txt")
    test_y = os.path.join(base_path, "test", "y_test.txt")

    if not (os.path.exists(train_x) and os.path.exists(train_y) and os.path.exists(test_x) and os.path.exists(test_y)):
        raise FileNotFoundError(
            f"Dataset files not found under {base_path}. Ensure UCI HAR Dataset is in current directory."
        )

    X_train = np.loadtxt(train_x)
    y_train = np.loadtxt(train_y, dtype=int).ravel()
    X_test = np.loadtxt(test_x)
    y_test = np.loadtxt(test_y, dtype=int).ravel()
    return X_train, y_train, X_test, y_test


def euclidean_distances(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute squared Euclidean distances between rows of a and rows of b."""
    #Your code goes here
    a1 = np.sum(a**2, axis=1).reshape(-1, 1)
    b1 = np.sum(b**2, axis=1).reshape(1, -1)
    ab = np.dot(a, b.T)
    return a1 + b1 - 2 * ab


def majority_vote(neighbor_labels: np.ndarray, neighbor_distances: np.ndarray) -> int:
    """
    neighbor_labels: array of labels of k nearest neighbors
    neighbor_distances: array of distances corresponding to label
    Returns the majority label. In case of tie, pick the label whose closest
    neighbor among the tied labels is nearest.
    """
    #Your code goes here
    u, c = np.unique(neighbor_labels, return_counts=True)
    max_c = np.max(c)
    cand = u[c == max_c]

    if len(cand) == 1:
        return cand[0]
    else:
        min_dist = float('inf')
        chosen_label = -1
        for lbl in cand:
            dist = np.min(neighbor_distances[neighbor_labels == lbl])
            if dist < min_dist:
                min_dist = dist
                chosen_label = lbl
        return chosen_label

def confusion_matrix_multiclass(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Compute the confusion matrix
    Rows = true classes, Columns = predicted classes.
    """
    #Your code goes here
    classes = np.unique(np.concatenate((y_true, y_pred)))
    cm = np.zeros((len(classes), len(classes)), dtype=int)
    for i, true_label in enumerate(classes):
        for j, pred_label in enumerate(classes):
            cm[i, j] = np.sum((y_true == true_label) & (y_pred == pred_label))
    return cm
    
def display_confusion_matrix_and_accuracy(k: int, y_true: np.ndarray, y_pred: np.ndarray):
    """
    Display a readable confusion matrix table.
    """
    acc = accuracy(y_true, y_pred)
    print(f"k ={k:2d}  accuracy={acc*100:5.2f}%")
    cm = confusion_matrix_multiclass(y_true, y_pred)
    classes = np.unique(np.concatenate((y_true, y_pred)))

    print("Confusion Matrix:")
    print("True\\Pred", end="\t")
    for c in classes:
        print(f"{c}", end="\t")
    print()

    for i, c in enumerate(classes):
        print(f"{c}", end="\t\t")
        for j in range(len(classes)):
            print(f"{cm[i, j]}", end="\t")
        print()

def accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    #Your code goes here
    return np.sum(y_true == y_pred) / len(y_true)


class ScratchKNN:
    """KNN classifier from scratch with nearest-neighbor tie-breaking."""

    def __init__(self, k: int = 3):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.X_train = X
        self.y_train = y

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict labels for test samples.
        Uses full sorting to get k nearest neighbors.
        """
        #Your code goes here
        dist = euclidean_distances(X_test, self.X_train)
        pred = np.zeros(X_test.shape[0], dtype=int)
        idx = np.argsort(dist, axis=1)[:, :self.k]

        for i in range(X_test.shape[0]):
            label = self.y_train[idx[i]]
            neighbor_distances = dist[i, idx[i]]
            pred[i] = majority_vote(label, neighbor_distances)
        return pred