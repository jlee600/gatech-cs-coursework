from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np


def euclid_pairwise_dist(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    You implemented this in project 2! We'll give it to you here to save you the copypaste.
    Args:
        x: N x D numpy array
        y: M x D numpy array
    Return:
            dist: N x M array, where dist2[i, j] is the euclidean distance between
            x[i, :] and y[j, :]
    """
    x_norm = np.sum(x**2, axis=1, keepdims=True)
    yt = y.T
    y_norm = np.sum(yt**2, axis=0, keepdims=True)
    dist2 = np.abs(x_norm + y_norm - 2.0 * (x @ yt))
    return np.sqrt(dist2)


def confusion_matrix_vis(conf_matrix: np.ndarray):
    """
    Fancy print of confusion matrix. Just encapsulating some code out of the notebook.
    """
    _, ax = plt.subplots(figsize=(5, 5))
    ax.matshow(conf_matrix)
    ax.set_xlabel("Predicted Labels", fontsize=16)
    ax.xaxis.set_label_position("top")
    ax.set_ylabel("Actual Labels", fontsize=16)
    for (i, j), val in np.ndenumerate(conf_matrix):
        ax.text(
            j,
            i,
            str(val),
            ha="center",
            va="center",
            bbox=dict(boxstyle="round", facecolor="white", edgecolor="0.3"),
        )
    plt.show()
    return


class SMOTE(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """
        Generate the confusion matrix for the predicted labels of a classification task.
        This function should be able to process any number of unique labels, not just a binary task.

        The choice to put "true" and "predicted" on the left and top respectively is arbitrary.
        In other sources, you may see this format transposed.

        Args:
            y_true: (N,) array of true integer labels for the training points
            y_pred: (N,) array of predicted integer labels for the training points
            These vectors correspond along axis 0. y_pred[i] is the prediction for point i, whose true label is y_true[i].
            You can assume that the labels will be ints of the form [0, u).
        Return:
            conf_matrix: (u, u) array of ints containing instance counts, where u is the number of unique labels present
                conf_matrix[i,j] = the number of instances where a sample from the true class i was predicted to be in class j
        """
        u = np.max([np.max(y_true), np.max(y_pred)]) + 1
        conf_matrix = np.zeros((u, u), dtype=int)

        for i in range(len(y_true)):
            conf_matrix[y_true[i], y_pred[i]] += 1
        return conf_matrix


    @staticmethod
    def interpolate(
        start: np.ndarray, end: np.ndarray, inter_coeff: float
    ) -> np.ndarray:
        """
        Return an interpolated point along the line segment between start and end.

        Hint:
            if inter_coeff==0.0, this should return start;
            if inter_coeff==1.0, this should return end;
            if inter_coeff==0.5, this should return the midpoint between them;
            to generalize this behavior, try writing this out in terms of vector addition and subtraction
        Args:
            start: (D,) float array containing the start point
            end: (D,) float array containing the end point
            inter_coeff: (float) in [0,1] determining how far along the line segment the synthetic point should lie
        Return:
            interpolated: (D,) float array containing the new synthetic point along the line segment
        """
        return start + inter_coeff * (end - start)       

    @staticmethod
    def k_nearest_neighbors(points: np.ndarray, k: int) -> np.ndarray:
        """
        For each point, retrieve the indices of the k other points which are closest to that point.

        Hints:
            Find the pairwise distances using the provided function: euclid_pairwise_dist.
            For execution time, try to avoid looping over N, and use numpy vectorization to sort through the distances and find the relevant indices.
        Args:
            points: (N, D) float array of points
            k: (int) describing the number of neighbor indices to return
        Return:
            neighborhoods: (N, k) int array containing the indices of the nearest neighbors for each point
                neighborhoods[i, :] should be a k long 1darray containing the neighborhood of points[i]
                neighborhoods[i, 0] = j, such that points[j] is the closest point to points[i]
        """
        dist = euclid_pairwise_dist(points, points)
        np.fill_diagonal(dist, np.inf)
        return np.argsort(dist, axis=1)[:, :k]

    @staticmethod
    def smote(
        X: np.ndarray, y: np.ndarray, k: int, inter_coeff_range: Tuple[float]
    ) -> np.ndarray:
        """
        Perform SMOTE on the binary classification problem (X, y), generating synthetic minority points from the minority set.
        In 6.1, we did work for an arbitrary number of classes. Here, you can assume that our problem is binary, that y will only contain 0 or 1.

        Outline:
            # 1. Determine how many synthetic points are needed from which class label.
            # 2. Get the subset of the minority points.
            # 3. For each minority point, determine its neighborhoods. (call k_nearest_neighbors)
            # 4. Generate |maj|-|min| synthetic data points from that subset.
                # a. uniformly pick a random point as the start point
                # b. uniformly pick a random neighbor as the endpoint
                # c. uniformly pick a random interpolation coefficient from the provided range: `inter_coeff_range`
                # d. interpolate and add to output (call interpolate)
            # 5. Generate the class labels for these new points.
        Args:
            X: (|maj|+|min|, D) float array of points, containing both majority and minority points; corresponds index-wise to y
            y: (|maj|+|min|,) int array of class labels, such that y[i] is the class of X[i, :]
            k: (int) determines the size of the neighborhood around the sampled point from which to sample the second point
            inter_coeff_range: (a, b) determines the range from which to uniformly sample the interpolation coefficient
                Sample U[a, b)
                You can assume that 0 <= a < b <= 1
        Return:
            A tuple containing:
                - synthetic_X: (|maj|-|min|, D) float array of new, synthetic points
                - synthetic_y: (|maj|-|min|,) array of the labels of the new synthetic points
        """
        c = np.bincount(y)
        minc = np.argmin(c)
        maj = np.argmax(c)
        syn = c[maj] - c[minc]

        minp = X[y == minc]
        neighbors = SMOTE.k_nearest_neighbors(minp, k)
        
        synthetic_X = np.zeros((syn, X.shape[1]))
        synthetic_y = np.full(syn, minc)
        a, b = inter_coeff_range
        
        for i in range(syn):
            idx1 = np.random.randint(0, len(minp))
            start_point = minp[idx1]
            
            idx3 = np.random.choice(neighbors[idx1])
            idx2 = minp[idx3]
            
            temp = np.random.uniform(a, b)
            synthetic_X[i] = SMOTE.interpolate(start_point, idx2, temp)
            
        return synthetic_X, synthetic_y  

    @staticmethod
    def threshold_eval(y_true, y_pred, threshold) -> tuple[float, float]:
        """
        Calculate the False Positive Rate (FPR) and True Positive Rate (TPR) for a given (single) threshold.

        The threshold for the ROC curve is the value of the prediction at which we consider a point to be positive.
        For each threshold, we can calculate the true positive rate and false positive rate.

        Args:
            y_true: (N,) array or list of true integer labels
            y_pred: (N,) array or list of predicted float probabilities
            threshold: (float) in [0, 1] which determines the cutoff for classification

        Returns:
            A tuple containing the FPR and TPR for the given threshold.
            Mind the order of the return values (FPR, TPR).
        """
        y = (y_pred >= threshold).astype(int)
        conf_matrix = SMOTE.generate_confusion_matrix(y_true, y)

        tp = conf_matrix[1, 1]
        fp = conf_matrix[0, 1]
        tn = conf_matrix[0, 0]
        fn = conf_matrix[1, 0]

        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        return fpr, tpr

    @staticmethod
    def generate_roc(y_true, y_pred) -> list[Tuple[float, float]]:
        """
        Generate the sorted list of (FPR, TPR) points for the ROC Curve.

        The thresholds at which to evaluate the FPR and TPR are determined by the unique values in y_pred.
        This will generate precise ROC curve points, as the TPR and FPR will ony change at these values.

        In the threshold values ensure that you add, 0.0 and a value which is slightly greater that maximum probability
        to the unique values of y_pred.
        This will ensure that the edges cases of the ROC curve are covered.

        Since we want to model the Receiver Operating Characteristic (ROC) curve using the output of this function,
        FPR must be sorted in the ascending order. However, in the case of multiple points having the same FPR,
        we must further sort them by TPR in ascending order. This is important because the ROC curve should
        always move upwards when FPR remains constant.

        If the FPR values are not sorted correctly, the ROC will be misaligned and the curve will be having an incorrect shape
        which will lead to incorrect AUC value. Additionally, the corresponding TPR and threshold values must be aligned index-wise with
        their respective FPR values.

        This will ensure the correct plotting of the ROC curve and the accurate value of AUC.


        Args:
            y_true: (N,) array of true integer labels for the training points
            y_pred: (N,) array of predicted labels for the training points

        Returns:
            A list of (FPR, TPR) tuples, sorted by FPR and then TPR in ascending order to model the ROC curve.
        """
        thres = np.unique(y_pred)
        thres = np.concatenate(([0.0], thres, [np.max(y_pred) + 1e-6]))

        roc = []
        for threshold in thres:
            fpr, tpr = SMOTE.threshold_eval(y_true, y_pred, threshold)
            roc.append((fpr, tpr))

        roc.sort(key=lambda x: (x[0], x[1]))
        return roc

    @staticmethod
    def integrate_curve(roc_points: List[Tuple[float, float]]) -> float:
        """
        Calculate the Area Under the Curve (AUC) by integrating the ROC curve.

        Args:
            roc_points: A sorted list of (FPR, TPR) tuples, represetning the ROC curve as produced by the function 'generate_roc'.

        Returns:
            AUC: (float) The value of the Area Under the Curve (AUC) for the given ROC curve.
        """
        fpr = np.array([p[0] for p in roc_points])
        tpr = np.array([p[1] for p in roc_points])
        # return np.trapz(tpr, fpr)
        return np.trapezoid(tpr, fpr)

    @staticmethod
    def plot_roc_auc(roc_points: List[Tuple[float, float]], auc: float):
        """
        Plot the ROC curve and display the AUC value of the curve.

        Args:
            roc_points A sorted list of (FPR, TPR) tuples, which represents the ROC AUC curve for the given data.
            auc: (float) The value of the Area Under the Curve (AUC) for the given ROC Curve.
        """
        fpr = np.array([p[0] for p in roc_points])
        tpr = np.array([p[1] for p in roc_points])
        fig, graph = plt.subplots(figsize=(8, 6))
        graph.plot(
            fpr,
            tpr,
            marker="o",
            linestyle="-",
            color="blue",
            label=f"ROC Curve (AUC = {auc:0.3f})",
        )
        graph.plot([0, 1], [0, 1], linestyle="--", color="red")
        graph.fill_between(fpr, tpr, color="blue", alpha=0.2)
        graph.set_title("Receiver Operating Characteristic (ROC) Curve")
        graph.set_xlabel("False Positive Rate (FPR)")
        graph.set_ylabel("True Positive Rate (TPR)")
        graph.legend()
        plt.show()
