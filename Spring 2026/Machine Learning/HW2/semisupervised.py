import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from tqdm import tqdm
SIGMA_CONST = 1e-06
LOG_CONST = 1e-20


def complete_(data):
    """    
    Find and return all rows in the data for which there is no missingness (nan).
    You should not use looping. Numpy supports indexing with Boolean arrays.
    
    Args:
        data: np.ndarray(N,D+1), data where the last column is the labels
    Return:
        labeled_complete: np.ndarray(?,D+1), the rows of data that have all features and a label
    """
    mask = np.isnan(data).any(axis=1)
    return data[~mask]


def incomplete_(data):
    """    
    Find and return all rows in the data for which there is missingness (nan) in the features, but not the label.
    You should not use looping. Numpy supports indexing with Boolean arrays.
    
    Args:
        data: np.ndarray(N,D+1), data where the last column is the labels
    Return:
        labeled_incomplete: np.ndarray(?,D+1), the rows of data that have a label but are missing at least 1 feature
    """
    fn = np.isnan(data[:, :-1]).any(axis=1)
    valid = ~np.isnan(data[:, -1])
    return data[fn & valid]


def unlabeled_(data):
    """    
    Find and return all rows in the data for which there is missingness (nan) in the label, but not the features.
    You should not use looping. Numpy supports indexing with Boolean arrays.
    
    Args:
        data: np.ndarray(N,D+1), data where the last column is the labels
    Return:
        unlabeled_complete: np.ndarray(?,D+1), the rows of data that have all features but are missing a label
    """
    valid = ~np.isnan(data[:, :-1]).any(axis=1)
    n = np.isnan(data[:, -1])
    return data[valid & n]


class CleanData:

    def __init__(self):
        pass

    def pairwise_dist_missingness_aware(self, x, y):
        """        
        A missingness-aware distance metric computes the Euclidean distance using only
        the features where both points have valid (non-NaN) values, then applies a
        correction factor to account for the missing features.
        
        The correction factor is sqrt(D/D_valid),
        where D_valid is the number of features where both points had valid (non-NaN) values.
        An example is worked out in the notebook.
        
        Args:
            x: np.ndarray(N,D), points
            y: np.ndarray(M,D), points
        Returns:
            dist_missingness_aware: N x M array, where dist[i, j] is the euclidean distance between
            x[i, :] and y[j, :] with a correction factor applied based on total number of features / non-nan values in X[i] and Y[i]
        Note:
            You are not permitted to use loops. Instead, use broadcasting tricks.
            You may use the large intermediate technique where first you broadcast up to (N,M,D) then sum over D.
            Of course, you will need to take care of nans. np.isnan and np.where will be especially useful.
        """
        d = x.shape[1]
        xval = (~np.isnan(x)).astype(float)
        yval = (~np.isnan(y)).astype(float)
        
        dval = np.dot(xval, yval.T)
        dval[dval == 0] = np.nan 
        
        xzero = np.nan_to_num(x)
        yzero = np.nan_to_num(y)
        
        xsum = np.dot(xzero**2, yval.T)
        ysum = np.dot(xval, (yzero**2).T)
        xy = np.dot(xzero, yzero.T)
        
        dist = xsum + ysum - 2 * xy
        temp = np.sqrt(d / dval)
        
        return np.sqrt(dist) * temp

    def __call__(self, incomplete_points, complete_points, K, **kwargs):
        """        
        This function should fill in missing feature values by sampling the
        average value for said features from the K-nearest neighbors of a data point.
        
        Args:
            incomplete_points: np.ndarray(N_incomplete, D+1), the incomplete labeled observations, labels at the end
            complete_points: np.ndarray(N_complete, D+1), the complete labeled observations, labels at the end
            K: int, corresponding to the number of nearest neighbors you should average over
        Return:
            imputed_data: np.ndarray(N_complete+N_incomplete, D+1), containing both the complete points and recently filled points (in that order)
        Starting Code:
            data = np.vstack((complete_points, incomplete_points))
            imputed_data = data.copy()  # write your computed values into this
            pw_dist = self.pairwise_dist_missingness_aware(data[:,:-1], data[:,:-1])
            unprocessed_neighbor_idxs = np.argsort(pw_dist, axis=1)
            ...
        Notes:
            1. You need to find the k-closest points that actually have the feature you're looking for.
               You should temporarily ignore points with the same missingness.
            2. Don't write into the data you're using. That would make this iterative.
               Write into a write-only copy, and return that at the end.
            3. Don't include the labels on the distance function.
               Categorical variables are ill-defined on Euclidean distance.
        """
        data = np.vstack((complete_points, incomplete_points))
        imputed_data = data.copy()
        pw_dist = self.pairwise_dist_missingness_aware(data[:,:-1], data[:,:-1])
        unprocessed_neighbor_idxs = np.argsort(pw_dist, axis=1)
        
        N_complete = complete_points.shape[0]
        total = data.shape[0]
        for i in range(N_complete, total):
            
            missing = np.where(np.isnan(data[i, :-1]))[0]
            for f in missing:
                found = 0
                vals = 0.0
                
                for idx in unprocessed_neighbor_idxs[i]:
                    if idx == i:
                        continue 
                        
                    if not np.isnan(data[idx, f]):
                        vals += data[idx, f]
                        found += 1
                        
                        if found == K:
                            break
                            
                if found > 0:
                    imputed_data[i, f] = vals / found
                    
        return imputed_data


def median_clean_data(data):
    """    
    A simpler approach, replace every NaN with the median of the column.
    
    Args:
        data: np.ndarray(N, D+1), data with missing features, but non-missing labels (last element)
    Return:
        imputed_data: np.ndarray(N, D+1), data with missingness imputed by the median
    Notes:
        When taking the median of any feature, do not count the NaN value.
    """
    imputed_data = data.copy()
    col_med = np.nanmedian(data, axis=0)
    idx = np.where(np.isnan(data))
    imputed_data[idx] = col_med[idx[1]]
    
    return imputed_data
