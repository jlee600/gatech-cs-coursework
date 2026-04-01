import java.util.Collection;
import java.util.HashSet;
import java.util.NoSuchElementException;
import java.util.Set;

/**
 * Your implementation of an AVL.
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
public class AVL<T extends Comparable<? super T>> {
    // Do not add new instance variables or modify existing ones.
    private AVLNode<T> root;
    private int size;

    /**
     * Constructs a new AVL.
     *
     * This constructor should initialize an empty AVL.
     *
     * Since instance variables are initialized to their default values, there
     * is no need to do anything for this constructor.
     */
    public AVL() {
        // DO NOT IMPLEMENT THIS CONSTRUCTOR!
    }

    /**
     * Constructs a new AVL.
     *
     * This constructor should initialize the AVL with the data in the
     * Collection. The data should be added in the same order it is in the
     * Collection.
     *
     * @param data the data to add to the tree
     * @throws java.lang.IllegalArgumentException if data or any element in data
     *                                            is null
     */
    public AVL(Collection<T> data) {
        if (data == null) {
            throw new IllegalArgumentException("Invalid input");
        }
        for (T element: data) {
            if (element == null) {
                throw new IllegalArgumentException("Invalid input");
            }
            add(element);
        }
    }

    /**
     * Adds the element to the tree.
     *
     * Start by adding it as a leaf like in a regular BST and then rotate the
     * tree as necessary.
     *
     * If the data is already in the tree, then nothing should be done (the
     * duplicate shouldn't get added, and size should not be incremented).
     *
     * Remember to recalculate heights and balance factors while going back
     * up the tree after adding the element, making sure to rebalance if
     * necessary.
     *
     * Hint: Should you use value equality or reference equality?
     *
     * @param data the data to add
     * @throws java.lang.IllegalArgumentException if data is null
     */
    public void add(T data) {
        if (data == null) {
            throw new IllegalArgumentException("Invalid Input");
        }
        root = addHelper(root, data);
    }

    /**
     *
     * @param curr current node
     * @return the updated curr
     */
    private AVLNode<T> updateNode(AVLNode<T> curr) {
        int left = -1;
        int right = -1;
        if (curr.getLeft() != null) {
            left = curr.getLeft().getHeight();
        }
        if (curr.getRight() != null) {
            right = curr.getRight().getHeight();
        }
        curr.setBalanceFactor(left - right);
        curr.setHeight(Math.max(left, right) + 1);

        return curr;
    }
    /**
     *
     * @param curr curr node of the tree
     * @param data data to add
     * @return the updated node
     */
    private AVLNode<T> addHelper(AVLNode<T> curr, T data) {
        if (curr == null) {
            curr = new AVLNode<>(data);
            size++;
            return curr;
        }
        int compared = data.compareTo(curr.getData());
        if (compared < 0) {
            curr.setLeft(addHelper(curr.getLeft(), data));
        } else if (compared > 0) {
            curr.setRight(addHelper(curr.getRight(), data));
        }
        updateNode(curr);
        if (curr.getBalanceFactor() == 2) {
            if (curr.getLeft().getBalanceFactor() == -1) {
                curr.setLeft(leftRotation(curr.getLeft()));
            }
            curr = rightRotation(curr);
        } else if (curr.getBalanceFactor() == -2) {
            if (curr.getRight().getBalanceFactor() == 1) {
                curr.setRight(rightRotation(curr.getRight()));
            }
            curr = leftRotation(curr);
        }
        return curr;
    }

    /**
     *
     * @param curr current node
     * @return curr.right
     */
    private AVLNode<T> leftRotation(AVLNode<T> curr) {
        AVLNode<T> right = curr.getRight();
        curr.setRight(right.getLeft());
        right.setLeft(curr);
        updateNode(curr);
        updateNode(right);
        return right;
    }

    /**
     *
     * @param curr current node
     * @return updated curr
     */
    private AVLNode<T> rightRotation(AVLNode<T> curr) {
        AVLNode<T> left = curr.getLeft();
        curr.setLeft(left.getRight());
        left.setRight(curr);
        updateNode(curr);
        updateNode(left);
        return left;
    }

    /**
     * Removes and returns the element from the tree matching the given
     * parameter.
     *
     * There are 3 cases to consider:
     * 1: The node containing the data is a leaf (no children). In this case,
     * simply remove it.
     * 2: The node containing the data has one child. In this case, simply
     * replace it with its child.
     * 3: The node containing the data has 2 children. Use the successor to
     * replace the data, NOT predecessor. As a reminder, rotations can occur
     * after removing the successor node.
     *
     * Remember to recalculate heights and balance factors while going back
     * up the tree after removing the element, making sure to rebalance if
     * necessary.
     *
     * Do not return the same data that was passed in. Return the data that
     * was stored in the tree.
     *
     * Hint: Should you use value equality or reference equality?
     *
     * @param data the data to remove
     * @return the data that was removed
     * @throws java.lang.IllegalArgumentException if data is null
     * @throws java.util.NoSuchElementException   if the data is not found
     */
    public T remove(T data) {
        if (data == null) {
            throw new IllegalArgumentException("Invalid Input");
        }
        AVLNode<T> dummy = new AVLNode<>(null);
        root = removeHelper(root, data, dummy);
        return dummy.getData();
    }
    /**
     *
     * @param curr the current node
     * @param data the data to remove
     * @param dummy the dummy to store the removed data
     * @return the updated node
     */
    private AVLNode<T> removeHelper(AVLNode<T> curr, T data, AVLNode<T> dummy) {
        if (curr == null) {
            throw new NoSuchElementException("Element not found");
        }
        int compared = data.compareTo(curr.getData());
        if (compared < 0) {
            curr.setLeft(removeHelper(curr.getLeft(), data, dummy));
        } else if (compared > 0) {
            curr.setRight(removeHelper(curr.getRight(), data, dummy));
        } else {
            //data found
            dummy.setData(curr.getData());
            size--;
            //curr has no child
            if (curr.getLeft() == null && curr.getRight() == null) {
                return null;
            }
            //curr has one child
            if (curr.getLeft() != null && curr.getRight() == null) {
                return curr.getLeft();
            } else if (curr.getLeft() == null && curr.getRight() != null) {
                return curr.getRight();
            } else {
                //curr has two children
                AVLNode<T> dummy2 = new AVLNode<>(null);
                curr.setRight(removeSuccessor(curr.getRight(), dummy2));
                curr.setData(dummy2.getData());
            }
        }
        updateNode(curr);
        if (curr.getBalanceFactor() == 2) {
            if (curr.getLeft().getBalanceFactor() == -1) {
                curr.setLeft(leftRotation(curr.getLeft()));
            }
            curr = rightRotation(curr);
        } else if (curr.getBalanceFactor() == -2) {
            if (curr.getRight().getBalanceFactor() == 1) {
                curr.setRight(rightRotation(curr.getRight()));
            }
            curr = leftRotation(curr);
        }
        return curr;
    }
    /**
     *
     * @param curr the current node
     * @param dummy the dummy to store the successor
     * @return the updated node
     */
    private AVLNode<T> removeSuccessor(AVLNode<T> curr, AVLNode<T> dummy) {
        if (curr.getLeft() == null) {
            dummy.setData(curr.getData());
            return curr.getRight();
        } else {
            curr.setLeft(removeSuccessor(curr.getLeft(), dummy));
        }
        updateNode(curr);
        if (curr.getBalanceFactor() == 2) {
            if (curr.getLeft().getBalanceFactor() == -1) {
                curr.setLeft(leftRotation(curr.getLeft()));
            }
            curr = rightRotation(curr);
        } else if (curr.getBalanceFactor() == -2) {
            if (curr.getRight().getBalanceFactor() == 1) {
                curr.setRight(rightRotation(curr.getRight()));
            }
            curr = leftRotation(curr);
        }
        return curr;
    }

    /**
     * Returns the element from the tree matching the given parameter.
     *
     * Do not return the same data that was passed in. Return the data that
     * was stored in the tree.
     *
     * Hint: Should you use value equality or reference equality?
     *
     * @param data the data to search for in the tree
     * @return the data in the tree equal to the parameter
     * @throws java.lang.IllegalArgumentException if data is null
     * @throws java.util.NoSuchElementException   if the data is not in the tree
     */
    public T get(T data) {
        return getHelper(root, data);
    }
    /**
     *
     * @param curr the current node
     * @param data the date to search for
     * @return the data in the tree equal to the parameter
     */
    private T getHelper(AVLNode<T> curr, T data) {
        if (data == null) {
            throw new IllegalArgumentException("Invalid input");
        }
        if (curr == null) {
            throw new NoSuchElementException("Data not found in the tree");
        }
        int compared = data.compareTo(curr.getData());
        if (compared == 0) {
            return curr.getData();
        } else if (compared < 0) {
            return getHelper(curr.getLeft(), data);
        } else {
            return getHelper(curr.getRight(), data);
        }
    }

    /**
     * Returns whether or not data matching the given parameter is contained
     * within the tree.
     *
     * Hint: Should you use value equality or reference equality?
     *
     * @param data the data to search for in the tree.
     * @return true if the parameter is contained within the tree, false
     * otherwise
     * @throws java.lang.IllegalArgumentException if data is null
     */
    public boolean contains(T data) {
        if (data == null) {
            throw new IllegalArgumentException("Invalid Input");
        }
        return containsHelper(root, data);
    }

    /**
     *
     * @param curr current node of the tree
     * @param data data to compare
     * @return whether data is in the tree or not
     */
    private boolean containsHelper(AVLNode<T> curr, T data) {
        if (curr == null) {
            return false;
        }
        int compared = data.compareTo(curr.getData());
        if (compared < 0) {
            return containsHelper(curr.getLeft(), data);
        } else if (compared > 0) {
            return containsHelper(curr.getRight(), data);
        } else {
            return true;
        }
    }

    /**
     * Returns the height of the root of the tree.
     *
     * Should be O(1).
     *
     * @return the height of the root of the tree, -1 if the tree is empty
     */
    public int height() {
        return root == null ? -1 : root.getHeight();
    }

    /**
     * Clears the tree.
     *
     * Clears all data and resets the size.
     */
    public void clear() {
        root = null;
        size = 0;
    }

    /**
     * Find all elements within a certain distance from the given data.
     * "Distance" means the number of edges between two nodes in the tree.
     *
     * To do this, first find the data in the tree. Keep track of the distance
     * of the current node on the path to the data (you can use the return
     * value of a helper method to denote the current distance to the target
     * data - but note that you must find the data first before you can
     * calculate this information). After you have found the data, you should
     * know the distance of each node on the path to the data. With that
     * information, you can determine how much farther away you can traverse
     * from the main path while remaining within distance of the target data.
     *
     * Use a HashSet as the Set you return. Keep in mind that since it is a
     * Set, you do not have to worry about any specific order in the Set.
     * 
     * This must be implemented recursively.
     *
     * Ex:
     * Given the following AVL composed of Integers
     *              50
     *            /    \
     *         25      75
     *        /  \     / \
     *      13   37  70  80
     *    /  \    \      \
     *   12  15    40    85
     *  /
     * 10
     * elementsWithinDistance(37, 3) should return the set {12, 13, 15, 25,
     * 37, 40, 50, 75}
     * elementsWithinDistance(85, 2) should return the set {75, 80, 85}
     * elementsWithinDistance(13, 1) should return the set {12, 13, 15, 25}
     *
     * @param data     the data to begin calculating distance from
     * @param distance the maximum distance allowed
     * @return the set of all data within a certain distance from the given data
     * @throws java.lang.IllegalArgumentException if data is null
     * @throws java.util.NoSuchElementException   is the data is not in the tree
     * @throws java.lang.IllegalArgumentException if distance is negative
     */
    public Set<T> elementsWithinDistance(T data, int distance) {
        if (data == null) {
            throw new IllegalArgumentException("Invalid Input");
        }
        if (distance < 0) {
            throw new IllegalArgumentException("Distance can't be negative");
        }
        Set<T> orderl = new HashSet<>();
        distanceHelper(root, data, distance, orderl);
        return orderl;
    }

    /**
     *
     * @param curr current node
     * @param data data to search for
     * @param distance distance from the data
     * @param orderlist set of nodes within the distance from the data
     * @return orderlist
     */
    private int distanceHelper(AVLNode<T> curr, T data, int distance, Set<T> orderlist) {
        int distToNode;
        if (curr == null) {
            throw new NoSuchElementException("Data not found in the tree");
        }
        int compared = data.compareTo(curr.getData());
        if (compared == 0) {
            distToNode = 0;
        } else if (compared < 0) {
            distToNode = distanceHelper(curr.getLeft(), data, distance, orderlist) + 1;
        } else {
            distToNode = distanceHelper(curr.getRight(), data, distance, orderlist) + 1;
        }
        if (distToNode <= distance) {
            orderlist.add(curr.getData());
            if (data.compareTo(curr.getData()) <= 0) {
                helper2(curr.getRight(), distToNode + 1, distance, orderlist);
            }
            if (data.compareTo(curr.getData()) >= 0) {
                helper2(curr.getLeft(), distToNode + 1, distance, orderlist);
            }
        }
        return distToNode;
    }

    /**
     *
     * @param curr current node
     * @param distToNode current distance from the data
     * @param distance maximum distacne from the data
     * @param orderlist the set of data within the distance
     * @return orderlist
     */
    private Set<T> helper2(AVLNode<T> curr, int distToNode, int distance, Set<T> orderlist) {
        if (curr != null && distToNode <= distance) {
            orderlist.add(curr.getData());
            if (distToNode < distance) {
                helper2(curr.getLeft(), distToNode + 1, distance, orderlist);
                helper2(curr.getRight(), distToNode + 1, distance, orderlist);
            }
        }
        return orderlist;
    }


    /**
     * Returns the root of the tree.
     *
     * For grading purposes only. You shouldn't need to use this method since
     * you have direct access to the variable.
     *
     * @return the root of the tree
     */
    public AVLNode<T> getRoot() {
        // DO NOT MODIFY THIS METHOD!
        return root;
    }

    /**
     * Returns the size of the tree.
     *
     * For grading purposes only. You shouldn't need to use this method since
     * you have direct access to the variable.
     *
     * @return the size of the tree
     */
    public int size() {
        // DO NOT MODIFY THIS METHOD!
        return size;
    }
}
