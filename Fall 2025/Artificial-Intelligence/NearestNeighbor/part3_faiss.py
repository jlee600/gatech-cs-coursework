"""
Part 3: Scaling KNN with FAISS
Run: python part3_faiss.py
Compares sklearn KNN (for a chosen k) with FAISS L2 search + majority vote.
Note: FAISS may need to be installed. If faiss is not available, the script will explain how to install it.
"""
import time
import numpy as np
from utils import load_har_dataset, accuracy, majority_vote, ScratchKNN

def scratch_knn_time_and_acc(X_tr, y_tr, X_ts, y_ts, k=5):
    t0 = time.time()

    # Your code goes here
    knn = ScratchKNN(k)
    knn.fit(X_tr, y_tr)
    pred = knn.predict(X_ts)
    acc = accuracy(y_ts, pred)

    t1 = time.time()
    return (t1 - t0), acc

def faiss_knn_time_and_acc(X_tr, y_tr, X_ts, y_ts, k=5):
    try:
        import faiss
    except Exception as e:
        raise ImportError("faiss not found. Install with e.g. 'pip install faiss-cpu'") from e

    t0 = time.time()

    # Your code goes here
    pred = np.zeros(X_ts.shape[0], dtype=int)
    idx= faiss.IndexFlatL2(X_tr.shape[1])
    idx.add(X_tr.astype(np.float32))

    d1, i2 = idx.search(X_ts.astype(np.float32), k)
    for i in range(X_ts.shape[0]):
        label = y_tr[i2[i]]
        dist = d1[i]
        pred[i] = majority_vote(label, dist)
    
    acc = accuracy(y_ts, pred)
    
    t1 = time.time()
    return (t1 - t0), acc

def main():
    print("Part 3: FAISS scaling comparison")
    X_train, y_train, X_test, y_test = load_har_dataset()

    for k in [4, 6, 10, 20]:
        try:
            sk_time, sk_acc = scratch_knn_time_and_acc(X_train, y_train, X_test, y_test, k=k)
            print(f"scratch KNN k={k}: time={sk_time:.3f}s acc={sk_acc*100:.2f}%")
        except Exception as e:
            print("scratch KNN failed:", e)
            sk_time, sk_acc = None, None

        try:
            fa_time, fa_acc = faiss_knn_time_and_acc(X_train, y_train, X_test, y_test, k=k)
            print(f"faiss  k={k}: time={fa_time:.3f}s acc={fa_acc*100:.2f}%")
        except ImportError as e:
            print(str(e))
            fa_time, fa_acc = None, None

        print("-"*40)

if __name__ == '__main__':
    main()