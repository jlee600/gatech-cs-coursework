"""
Part 1: KNN from scratch
Run: python part1_knn_scratch.py
This will:
 - load the HAR dataset (expecting the "UCI HAR Dataset" folder in the current dir)
 - run the scratch KNN from util.py for k = 4,6
 - display the confusion matrix and accuracy
"""

from utils import load_har_dataset, ScratchKNN, display_confusion_matrix_and_accuracy

def main():
    print("Part 1: KNN from scratch")
    
    #Your code goes here
    xtrain, ytrain, xtest, ytest = load_har_dataset()
    for k in [4, 6]:
        knn = ScratchKNN(k)
        knn.fit(xtrain, ytrain)
        display_confusion_matrix_and_accuracy(k, ytest, knn.predict(xtest))

if __name__ == '__main__':
    main()
