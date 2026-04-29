import numpy as np
from sklearn.svm import SVC


def feature_construction(X: np.ndarray) -> np.ndarray:
    """
    Given the data, perform some transformation that will make the data linearly separable.

    Arguments:
        X: (10, 2) np.array - The data shown in the notebook.
    Returns:
        X_aug: (10, D) np.array - Some transformation of the data
    Hints:
        - The data may come shuffled, so don't handcode anything with specific indices.
        - Adding more features can't hurt separability. While you can carefully construct a great 1 feature boundary, it may be easier to just construct additional features.
    """
    x1 = X[:, 0]
    x2 = X[:, 1]
    x1_squared = x1 ** 2
    x2_squared = x2 ** 2
    return np.column_stack((x1, x2, x1_squared, x2_squared))


def kernel_construction(X: np.ndarray, phi: callable) -> np.ndarray:
    """
    Given a dataset and a callable feature map, construct a kernel matrix, K.
    Simply, K[i,j] = phi(x_i) . phi(x_j)

    Args:
        X: np.ndarray(N, D)[float]; the dataset
        phi: callable; takes (D,) returns (D',), some feature engineering map
    Returns:
        K: np.ndarray(N, N)[float]; the resultant kernel
    Hints:
        - You can do smart broadcasting or symmetric speedup, or you can just loop and calculate elementwise.
    """
    x = np.array([phi(x_i) for x_i in X])
    return np.dot(x, x.T)


def rbf_kernel(X: np.ndarray, gamma: float) -> np.ndarray:
    """
    Given a dataset and the gamma hyperparameter, build the radial basis function kernel.
    K[i, j] = exp(-gamma * ||x_i - x_j||^2)

    Args:
        X: np.ndarray(N, D)[float]; the dataset
        gamma: float; a hyperparameter for the RBF kernel
    Returns:
        K: np.ndarray(N, N)[float]; the resultant kernel
    Hints:
        - You can do smart broadcasting or symmetric speedup, or you can just loop and calculate elementwise.
    """
    norms = np.sum(X ** 2, axis=1, keepdims=True)
    dist = norms + norms.T - 2 * np.dot(X, X.T)
    return np.exp(-gamma * dist)
