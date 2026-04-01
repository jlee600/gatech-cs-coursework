import java.util.Comparator;
import java.util.Random;
import java.util.LinkedList;
import java.util.PriorityQueue;
import java.util.List;

/**
 * Your implementation of various sorting algorithms.
 *
 * @author Jinseo Lee
 * @version 1.0
 * @userid jlee4223
 * @GTID 903950086
 *
 * Collaborators: LIST ALL COLLABORATORS YOU WORKED WITH HERE
 *
 * Resources: LIST ALL NON-COURSE RESOURCES YOU CONSULTED HERE
 */
public class Sorting {

    /**
     *
     * @param arr array to sort
     * @param a element to swap with b
     * @param b element to swap with a
     * @param <T> data type to sort
     */
    private static <T> void swap(T[] arr, int a, int b) {
        T temp = arr[a];
        arr[a] = arr[b];
        arr[b] = temp;
    }

    /**
     * Implement selection sort.
     *
     * It should be:
     * in-place
     * unstable
     * not adaptive
     *
     * Have a worst case running time of:
     * O(n^2)
     *
     * And a best case running time of:
     * O(n^2)
     *
     * @param <T>        data type to sort
     * @param arr        the array that must be sorted after the method runs
     * @param comparator the Comparator used to compare the data in arr
     * @throws java.lang.IllegalArgumentException if the array or comparator is
     *                                            null
     */
    public static <T> void selectionSort(T[] arr, Comparator<T> comparator) {
        if (arr == null || comparator == null) {
            throw new IllegalArgumentException("Invalid Input");
        }
        if (arr.length == 1) {
            return;
        }
        int n = arr.length;
        for (int i = n - 1; i > 0; i--) {
            int maxidx = i;
            for (int j = 0; j < i; j++) {
                if (comparator.compare(arr[j], arr[maxidx]) > 0) {
                    maxidx = j;
                }
            }
            swap(arr, maxidx, i);
        }
    }

    /**
     * Implement cocktail sort.
     *
     * It should be:
     * in-place
     * stable
     * adaptive
     *
     * Have a worst case running time of:
     * O(n^2)
     *
     * And a best case running time of:
     * O(n)
     *
     * NOTE: See pdf for last swapped optimization for cocktail sort. You
     * MUST implement cocktail sort with this optimization
     *
     * @param <T>        data type to sort
     * @param arr        the array that must be sorted after the method runs
     * @param comparator the Comparator used to compare the data in arr
     * @throws java.lang.IllegalArgumentException if the array or comparator is
     *                                            null
     */
    public static <T> void cocktailSort(T[] arr, Comparator<T> comparator) {
        if (arr == null || comparator == null) {
            throw new IllegalArgumentException("Invalid Input");
        }
        if (arr.length == 1) {
            return;
        }

        int startidx = 0;
        int endidx = arr.length - 1;

        while (startidx < endidx) {
            int isSwapped = 0;
            for (int i = startidx; i < endidx; i++) {
                if (comparator.compare(arr[i], arr[i + 1]) > 0) {
                    swap(arr, i, i + 1);
                    isSwapped = i;
                }
            }
            endidx = isSwapped;
            for (int i  = endidx; i > startidx; i--) {
                if (comparator.compare(arr[i - 1], arr[i]) > 0) {
                    swap(arr, i, i - 1);
                    isSwapped = i;
                }
            }
            startidx = isSwapped;
        }
    }

    /**
     * Implement merge sort.
     *
     * It should be:
     * out-of-place
     * stable
     * not adaptive
     *
     * Have a worst case running time of:
     * O(n log n)
     *
     * And a best case running time of:
     * O(n log n)
     *
     * You can create more arrays to run merge sort, but at the end, everything
     * should be merged back into the original T[] which was passed in.
     *
     * When splitting the array, if there is an odd number of elements, put the
     * extra data on the right side.
     *
     * Hint: If two data are equal when merging, think about which subarray
     * you should pull from first
     *
     * @param <T>        data type to sort
     * @param arr        the array to be sorted
     * @param comparator the Comparator used to compare the data in arr
     * @throws java.lang.IllegalArgumentException if the array or comparator is
     *                                            null
     */
    public static <T> void mergeSort(T[] arr, Comparator<T> comparator) {
        if (arr == null || comparator == null) {
            throw new IllegalArgumentException("Invalid Input");
        }
        if (arr.length > 1) {
            int mididx = arr.length / 2;
            T[] leftArr = (T[]) new Object[mididx];
            T[] rightArr = (T[]) new Object[arr.length - mididx];
            for (int i = 0; i < mididx; i++) {
                leftArr[i] = arr[i];
            }
            for (int i = mididx; i < arr.length; i++) {
                rightArr[i - mididx] = arr[i];
            }
            mergeSort(leftArr, comparator);
            mergeSort(rightArr, comparator);

            int i = 0;
            int j = 0;
            while (i < mididx && j < arr.length - mididx) {
                if (comparator.compare(leftArr[i], rightArr[j]) <= 0) {
                    arr[i + j] = leftArr[i];
                    i++;
                } else {
                    arr[i + j] = rightArr[j];
                    j++;
                }
            }
            while (i < leftArr.length) {
                arr[i + j] = leftArr[i];
                i++;
            }
            while (j < rightArr.length) {
                arr[i + j] = rightArr[j];
                j++;
            }
        }
    }

    /**
     * Implement kth select.
     *
     * Use the provided random object to select your pivots. For example if you
     * need a pivot between a (inclusive) and b (exclusive) where b > a, use
     * the following code:
     *
     * int pivotIndex = rand.nextInt(b - a) + a;
     *
     * If your recursion uses an inclusive b instead of an exclusive one,
     * the formula changes by adding 1 to the nextInt() call:
     *
     * int pivotIndex = rand.nextInt(b - a + 1) + a;
     *
     * It should be:
     * in-place
     *
     * Have a worst case running time of:
     * O(n^2)
     *
     * And a best case running time of:
     * O(n)
     *
     * You may assume that the array doesn't contain any null elements.
     *
     * Make sure you code the algorithm as you have been taught it in class.
     * There are several versions of this algorithm and you may not get full
     * credit if you do not implement the one we have taught you!
     *
     * @param <T>        data type to sort
     * @param k          the index to retrieve data from + 1 (due to
     *                   0-indexing) if the array was sorted; the 'k' in "kth
     *                   select"; e.g. if k == 1, return the smallest element
     *                   in the array
     * @param arr        the array that should be modified after the method
     *                   is finished executing as needed
     * @param comparator the Comparator used to compare the data in arr
     * @param rand       the Random object used to select pivots
     * @return the kth smallest element
     * @throws java.lang.IllegalArgumentException if the array or comparator
     *                                            or rand is null or k is not
     *                                            in the range of 1 to arr
     *                                            .length
     */
    public static <T> T kthSelect(int k, T[] arr, Comparator<T> comparator,
                                  Random rand) {
        if (arr == null || comparator == null || rand == null) {
            throw new IllegalArgumentException("Invalid Input");
        }
        if (k < 1 || k > arr.length) {
            throw new IllegalArgumentException("K out of index");
        }
        return kthSelectHelper(k, arr, 0, arr.length - 1, comparator, rand);
    }

    /**
     *
     * @param k the index to retrieve data from + 1
     * @param arr the array that should be modified after the method
     *                               is finished executing as needed
     * @param left the startpoint
     * @param right the endpoint
     * @param comparator the Comparator used to compare the data in arr
     * @param rand the Random object used to select pivots
     * @return the kth smallest element
     * @param <T> data type to sort
     */
    private static <T> T kthSelectHelper(int k, T[] arr, int left, int right, Comparator<T> comparator, Random rand) {
        if (left == right) {
            return arr[left];
        }

        int pivotIndex = rand.nextInt(right - left + 1) + left;
        pivotIndex = partition(arr, left, right, pivotIndex, comparator);

        if (k - 1 == pivotIndex) {
            return arr[pivotIndex];
        } else if (k - 1 < pivotIndex) {
            return kthSelectHelper(k, arr, left, pivotIndex - 1, comparator, rand);
        } else {
            return kthSelectHelper(k, arr, pivotIndex + 1, right, comparator, rand);
        }
    }

    /**
     *
     * @param arr array to be modified
     * @param left the startpoint
     * @param right the endpoint
     * @param pivotIdx the index of the random pivot point
     * @param comparator the Comparator used to compare the data in arr
     * @return the new index of pivot point
     * @param <T> data type to sort
     */
    private static <T> int partition(T[] arr, int left, int right, int pivotIdx, Comparator<T> comparator) {
        T pivotVal = arr[pivotIdx];
        //swap first element and pivot
        swap(arr, left, pivotIdx);

        int i = left + 1;
        int j = right;
        while (i <= j) {
            while (i <= j && comparator.compare(arr[i], pivotVal) <= 0) {
                i++;
            }
            while (i <= j && comparator.compare(arr[j], pivotVal) >= 0) {
                j--;
            }
            if (i <= j) {
                // Swap i and j
                swap(arr, i, j);
                i++;
                j--;
            }
        }
        //swap j and pivot
        swap(arr, j, left);
        return j;
    }

    /**
     * Implement LSD (least significant digit) radix sort.
     *
     * Make sure you code the algorithm as you have been taught it in class.
     * There are several versions of this algorithm and you may not get full
     * credit if you do not implement the one we have taught you!
     *
     * Remember you CANNOT convert the ints to strings at any point in your
     * code! Doing so may result in a 0 for the implementation.
     *
     * It should be:
     * out-of-place
     * stable
     * not adaptive
     *
     * Have a worst case running time of:
     * O(kn)
     *
     * And a best case running time of:
     * O(kn)
     *
     * You are allowed to make an initial O(n) passthrough of the array to
     * determine the number of iterations you need. The number of iterations
     * can be determined using the number with the largest magnitude.
     *
     * At no point should you find yourself needing a way to exponentiate a
     * number; any such method would be non-O(1). Think about how how you can
     * get each power of BASE naturally and efficiently as the algorithm
     * progresses through each digit.
     *
     * Refer to the PDF for more information on LSD Radix Sort.
     *
     * You may use ArrayList or LinkedList if you wish, but it may only be
     * used inside radix sort and any radix sort helpers. Do NOT use these
     * classes with other sorts. However, be sure the List implementation you
     * choose allows for stability while being as efficient as possible.
     *
     * Do NOT use anything from the Math class except Math.abs().
     *
     * @param arr the array to be sorted
     * @throws java.lang.IllegalArgumentException if the array is null
     */
    public static void lsdRadixSort(int[] arr) {
        if (arr == null) {
            throw new IllegalArgumentException("Invalid Input");
        }
        if (arr.length == 0) {
            return;
        }
        //initialize buckets
        LinkedList<Integer>[] buckets = new LinkedList[19];
        //get the number with the max digit
        int max = getMax(arr);
        //get the max digit
        int maxDigits = countMax(max);

        int base = 1;
        for (int i = maxDigits; i > 0; i--, base *= 10) {
            //add num to buckets
            for (int num: arr) {
                int digitNeeded = ((num / base) % 10) + 9;
                //initialize empty linked-list if empty
                if (buckets[digitNeeded] == null) {
                    buckets[digitNeeded] = new LinkedList<>();
                }
                buckets[digitNeeded].addLast(num);
            }
            //remove from buckets & add back to array
            int idx = 0;
            for (int j = 0; j < buckets.length; j++) {
                if (buckets[j] != null) { //null pointer exception
                    while (!buckets[j].isEmpty()) {
                        arr[idx] = buckets[j].removeFirst();
                        idx++;
                    }
                }
            }
        }
    }

    /**
     *
     * @param arr array to sort
     * @return element with max number of digits
     */
    private static int getMax(int[] arr) {
        int max = Math.abs(arr[0]);
        for (int i = 1; i < arr.length; i++) {
            int cand = arr[i];
            if (cand == Integer.MIN_VALUE || cand == Integer.MAX_VALUE) {
                max = Integer.MAX_VALUE;
                break;
            }
            if (Math.abs(cand) > max) {
                max = Math.abs(cand);
            }
        }
        return max;
    }

    /**
     *
     * @param max element with max digit numebers
     * @return number of digits
     */
    private static int countMax(int max) {
        int maxDigits = 0;
        if (max != 0) {
            while (max >= 1) {
                max /= 10;
                maxDigits++;
            }
        } else {
            maxDigits = 1;
        }
        return maxDigits;
    }

    /**
     * Implement heap sort.
     *
     * It should be:
     * out-of-place
     * unstable
     * not adaptive
     *
     * Have a worst case running time of:
     * O(n log n)
     *
     * And a best case running time of:
     * O(n log n)
     *
     * Use java.util.PriorityQueue as the heap. Note that in this
     * PriorityQueue implementation, elements are removed from smallest
     * element to largest element.
     *
     * Initialize the PriorityQueue using its build heap constructor (look at
     * the different constructors of java.util.PriorityQueue).
     *
     * Return an int array with a capacity equal to the size of the list. The
     * returned array should have the elements in the list in sorted order.
     *
     * @param data the data to sort
     * @return the array with length equal to the size of the input list that
     * holds the elements from the list is sorted order
     * @throws java.lang.IllegalArgumentException if the data is null
     */
    public static int[] heapSort(List<Integer> data) {
        if (data == null) {
            throw new IllegalArgumentException("Invalid Input");
        }
        PriorityQueue<Integer> pQ = new PriorityQueue<>(data);
        int initSize = data.size();
        int[] arr = new int[initSize];
        for (int i = 0; i < initSize; i++) {
            arr[i] = pQ.remove();
        }
        return arr;
    }
}
