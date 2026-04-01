"""
Part 2: KNN using scikit-learn
Run: python part2_sklearn.py
Produces a PNG plot named accuracy_vs_k.png in the current directory.
"""

import numpy as np
from utils import load_har_dataset, display_confusion_matrix_and_accuracy, accuracy
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

def KNN_using_sklearn(X_train, y_train, X_test, y_test, k):
    # Your code goes here
    knn = KNeighborsClassifier(k)
    knn.fit(X_train, y_train)
    pred = knn.predict(X_test)
    acc = accuracy(y_test, pred)
    return pred, acc

def main():
    print("Part 2: KNN using scikit-learn")

    accs = []
    ks = []
        
    # Your code goes here
    xtrain, ytrain, xtest, ytest = load_har_dataset()
    kbest, accbest, predbest = None, -1, None

    for k in range(1, 11):
        pred, acc = KNN_using_sklearn(xtrain, ytrain, xtest, ytest, k)
        display_confusion_matrix_and_accuracy(k, ytest, pred)
        
        ks.append(k)
        accs.append(acc)
        # print(f"k={k:2d}, Accuracy={acc*100:.2f}%")

        if acc > accbest:
            kbest, accbest, predbest = k, acc, pred

    # print(f"\nBest k:{kbest}, best accuracy={accbest*100:.2f}%")
    display_confusion_matrix_and_accuracy(kbest, ytest, predbest)

    # Plot and save accuracy vs k
    plt.figure(figsize=(8,4))
    plt.plot(ks, [a*100 for a in accs], marker='o')
    plt.xlabel('k (number of neighbors)')
    plt.ylabel('Accuracy (%)')
    plt.title('KNN (sklearn) Accuracy vs k (sampled)')
    plt.grid(True)
    plt.savefig('accuracy_vs_k.png', bbox_inches='tight')
    print("Saved plot to accuracy_vs_k.png")

if __name__ == '__main__':
    main()
