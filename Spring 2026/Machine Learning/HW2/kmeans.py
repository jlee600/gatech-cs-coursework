import numpy as np
# from sklearn.discriminant_analysis import unique_labels
# from torch import dist


class KMeans(object):

    def __init__(self, points, k, init='random', max_iters=10000, rel_tol=1e-05
        ):
        """
        Args:
            points: np.ndarray(N,D), where N is # points and D is the dimensionality
            k: int, number of clusters
            init: str, how to initialize the centers
            max_iters: int, maximum number of iterations
            rel_tol: float, convergence criteria with respect to relative change of loss (number between 0 and 1)
        """
        self.points = points
        self.K = k
        if init == 'random':
            self.centers = self.init_centers()
        else:
            self.centers = self.kmpp_init()
        self.assignments = None
        self.loss = 0.0
        self.rel_tol = rel_tol
        self.max_iters = max_iters

    def init_centers(self):
        """        
        Initialize the centers randomly.
        Use np.random.choice to pick K indices from the integers [0, N) without replacement,
        then use those indices to index into self.points.
        
        Update:
            self.centers: np.ndarray(K,D), randomly selected centers
        Return:
            self.centers, set it and also return it
        Hints:
            Numpy will let you index an array with an iterable!
            It will vstack the subsequent results together into a resultant array.
            We won't stop you from looping here, but it's a cool trick to know.
        """
        n = self.points.shape[0]
        idx = np.random.choice(n, self.K, replace=False)
        self.centers = self.points[idx]
        return self.centers
        

    def kmpp_init(self):
        """        
        We can do better than random sampling!
        KMeans++ uses the intuition that good initial clusters will be further away from each other.
        
        1. Sample 1% of the points from the dataset, uniformly at random and without replacement.
            This sample will be the dataset the remainder of the algorithm uses to minimize initialization overhead.
        2. From the above sample, select only one random point to be the first cluster center.
        3. For each point in the sampled dataset, find the nearest cluster center and record the squared distance to get there.
        4. Examine all the squared distances and take the point with the maximum squared distance as a new cluster center.
            In other words, we will choose the next center by picking the most remote data point
            instead of sampling randomly like in step 2. You may break ties arbitrarily.
        5. Repeat 3-4 until all k-centers have been assigned. You may use a loop over K to keep track of the data in each cluster.
        
        Update:
            self.centers: np.ndarray(K,D), randomly selected centers
        Return:
            self.centers, set it and also return it
        """
        n = self.points.shape[0]
        s = max(1, n // 100)
        idx = np.random.choice(n, s, replace=False)
        sample_points = self.points[idx]

        self.centers = np.zeros((self.K, self.points.shape[1]))
        first_idx = np.random.choice(s, 1, replace=False)[0]
        self.centers[0] = sample_points[first_idx]
        
        for i in range(1, self.K):
            dist1 = pairwise_dist(sample_points, self.centers[:i]) ** 2
            dist2 = np.min(dist1, axis=1)
            next_center_idx = np.argmax(dist2)
            self.centers[i] = sample_points[next_center_idx]
        
        return self.centers

    def update_assignment(self):
        """        
        Assign each point to the cluster whose center is the closest to that point.
        
        Update:
            self.assignments: np.ndarray(N,), self.assignments[i] is the index of the cluster to which self.points[i,:] belongs
        Return:
            self.assignments, set it and also return it
        Note:
            Don't overwork here. Call your pairwise_dist and work with that data to find the closest center per point.
            Looping may cause timeouts here.
        """
        dist = pairwise_dist(self.points, self.centers)
        self.assignments = np.argmin(dist, axis=1)
        return self.assignments
    
    def update_centers(self):
        """        
        Update the positions of the cluster centers to be the centroid of all data in the cluster.
        
        Loop through each cluster's index, 0...k-1:
            Find the subset of points belonging to the cluster with self.assignments.
            If that subset is non-empty, calculate the centroid, and update self.centers with that value.
            If the subset is empty, we need to pick a new value. Using the current state of self.centers:
                1. Calculate the pairwise distance from every point in self.points to every center in self.centers.
                2. Find the point that is farthest away from every other center.
                3. Set the center for this empty to that lonely point.
        
        Update:
            self.centers: np.ndarray(K,D)[float], self.centers[i,:] should be the center for the i^th cluster
        Return:
            self.centers, set it and also return it
        Note:
            Points is non-typed. It might be an integer type. However, the dtype of the centers should definitely be a float.
                e.g., if your cluster has 1 and 2 in it, the center should be 1.5
            Watch out for dtype casting! You may get unexpected behavior.
        """
        center = np.zeros_like(self.centers)
        for i in range(self.K):
            cluster = self.points[self.assignments == i]
            if len(cluster) > 0:
                center[i] = np.mean(cluster, axis=0)
            else:
                dist = pairwise_dist(self.points, self.centers)
                dist[:, i] = np.inf
                close = np.min(dist, axis=1)
                far = np.argmax(close)
                center[i] = self.points[far]

        self.centers = center
        return self.centers

    def get_loss(self):
        """        
        The loss will be defined as the sum of the squared distances between each point and it's respective center.
        
        Update:
            self.loss: float, the objective function of KMeans
        Return:
            self.loss, set it and also return it
        """
        center = self.centers[self.assignments]
        self.loss = np.sum((self.points - center) ** 2)
        return self.loss

    def train(self):
        """        
        Train KMeans to cluster the data:
            0. Recall that self.centers have already been initialized in __init__
            1. Update the cluster assignment for each point (update_assignment)
            2. Update the cluster centers based on the new assignments (update_centers)
            3. Calculate the loss (get_loss) and check if the model has converged to break the loop early.
               - The convergence criteria is measured by whether the percentage difference
                 in loss compared to the previous iteration is less than the given
                 relative tolerance threshold (self.rel_tol).
               - Relative tolerance threshold (self.rel_tol) is a number between 0 and 1.
            4. Iterate through steps 1 to 3 at most max_iters times.
        
        Update:
            self.centers: np.ndarray(K,D)
            self.assignments: np.ndarray(N,)
            self.loss: float
            All of these values will be updated in the functions you already implemented, you just need to call them.
        Return:
            (self.centers, self.assignments, self.loss)
        Note:
            Do not loop over all the points in every iteration. This may result in time out errors.
        """
        l = None
        for _ in range(self.max_iters):
            self.update_assignment()
            self.update_centers()
            loss = self.get_loss()
            if l is not None:
                if abs(loss - l) / l < self.rel_tol:
                    break
            l = loss

        return self.centers, self.assignments, self.loss


def pairwise_dist(x, y):
    """    
    Calculates the Euclidean distance between every cross pair of points, one from each input.
    This function is to be space and time efficient.
    1. No looping, only numpy functions.
    2. No intermediate arrays larger than the output, e.g., (NxMxD).
    
    You'll need to follow the instructions in the notebook, where the Euclidean distance
    is expressed as a combination of several terms, sums of rows of X^2, sums of rows of Y^2,
    and a cross term containing the dot product of X[i, :] and Y[j, :]
    
    Args:
        x: np.ndarray(N,D), first set of points
        y: np.ndarray(M,D), second set of points
    Return:
        dist: np.ndarray(N,M), where dist[i, j] is the
            euclidean distance between x[i, :] and y[j, :]
    """
    x = np.asarray(x)
    y = np.asarray(y)
    x2 = np.sum(x ** 2, axis=1).reshape(-1, 1)
    y2 = np.sum(y ** 2, axis=1).reshape(1, -1)
    xy = np.dot(x, y.T)
    d2 = x2 + y2 - 2 * xy
    d2 = np.maximum(d2, 0)
    dist = np.sqrt(d2)
    return dist


def adjusted_rand_statistic(xGroundTruth, xPredicted):
    """    
    Calculate ARI by enumerating pairs of points and binning them by agreement.
    
    The idea is to make the comparison of Predicted and Ground truth data points.
        1. Iterate over all distinct pairs of points (looping is permitted!).
        2. Compare the prediction pair label with the ground truth pair.
        3. Based on the analysis, we can figure out whether both points fall under TP/FP/FN/FP
           i.e. if a pair falls under TP, increment by 2 (one for each point in the pair).
        4. Then calculate the adjusted rand index value
    
    Args:
        xPredicted: list of length N, the predicted cluster labels
        xGroundTruth: list of length N, the "correct" cluster labels
    Return:
        ARI: float, computed ARI value
    """
    tp = fp = fn = tn = 0
    n = len(xGroundTruth)

    for i in range(n):
        for j in range(i + 1, n):
            gt = xGroundTruth[i] == xGroundTruth[j]
            pred = xPredicted[i] == xPredicted[j]
            if gt and pred:
                tp += 1
            elif not gt and pred:
                fp += 1
            elif not gt and not pred:
                tn += 1
            else:
                fn += 1
    
    num = 2 * (tp * tn - fp * fn)
    den = (tp + fp) * (fp + tn) + (tp + fn) * (fn + tn)
    
    return num / den


def silhouette_score(X, labels):
    """    
    The idea is to calculate the mean distance between a point and the other points
    in its cluster (the intra cluster distance) and the mean distance between a point and the
    other points in its closest cluster (the inter cluster distance)
        1.  Calculate the pairwise_dist between all points to each other (N x N)
        2.  Loop over all points in the provided data (X) and for each point calculate:
    
            Intra Cluster Distances (point p to the other points in its own cluster)
                a. Identify all points in the same cluster as p (excluding p itself)
                b. Calculate the mean pairwise_dist between p and the other points
                c. If there are no other points in the same cluster, assign an
                   intra-cluster distance of 0
    
            Inter Cluster Distances (point p to the points in the closest cluster)
                a. Loop over all clusters except for p's cluster
                b. For each cluster, identify all points belonging to it
                c. Calculate the mean pairwise_dist between p and those points
                d. Set the inter-cluster distance to the minimum mean pairwise_dist
                   among all clusters. Again, if there are no other clusters, use
                   an inter-cluster distance of 0.
    
        3. Calculate the silhouette scores for each point using
                s_i = (mu_out(x_i) - mu_in(x_i)) / max(mu_out(x_i), mu_in(x_i))
        4. Average the silhouette score across all points
    
    Args:
        X: np.ndarray(N,D), the coordinates of the data
        labels: np.ndarray(N,), the corresponding labels of the data
    Return:
        silhouette score: final coefficient value of type np.float64
    Note:
        You can refer to the Clustering Evaluation slides from Lecture for additional info if needed
    """
    n = X.shape[0]
    dist = pairwise_dist(X, X)
    s = np.zeros(n)
    label = np.unique(labels)
    
    for i in range(n):
        idx = np.where(labels == labels[i])[0]
        a = np.sum(dist[i, idx]) / (len(idx) - 1)
        b = np.inf

        for l in label:
            if l == labels[i]:
                continue
            idx2 = np.where(labels == l)[0]

            if len(idx2) > 0:
                avg_dist = np.mean(dist[i, idx2])
                if avg_dist < b:
                    b = avg_dist
                    
        s[i] = (b - a) / max(a, b)
            
    return np.mean(s)
