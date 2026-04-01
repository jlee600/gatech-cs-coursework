import java.util.Collection;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;
import java.util.NoSuchElementException;

/**
 * Your implementation of a BST.
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
public class BST<T extends Comparable<? super T>> {

    /*
     * Do not add new instance variables or modify existing ones.
     */
    private BSTNode<T> root;
    private int size;

    /**
     * Constructs a new BST.
     *
     * This constructor should initialize an empty BST.
     *
     * Since instance variables are initialized to their default values, there
     * is no need to do anything for this constructor.
     */
    public BST() {
        // DO NOT IMPLEMENT THIS CONSTRUCTOR!
    }

    /**
     * Constructs a new BST.
     *
     * This constructor should initialize the BST with the data in the
     * Collection. The data should be added in the same order it is in the
     * Collection.
     *
     * Hint: Not all Collections are indexable like Lists, so a regular for loop
     * will not work here. However, all Collections are Iterable, so what type
     * of loop would work?
     *
     * @param data the data to add
     * @throws java.lang.IllegalArgumentException if data or any element in data
     *                                            is null
     */
    public BST(Collection<T> data) {
        if (data == null) {
            throw new IllegalArgumentException("Invalid input");
        }
        for (T element: data) {
            add(element);
        }
    }

    /**
     * Adds the data to the tree.
     *
     * This must be done recursively.
     *
     * The data becomes a leaf in the tree.
     *
     * Traverse the tree to find the appropriate location. If the data is
     * already in the tree, then nothing should be done (the duplicate
     * shouldn't get added, and size should not be incremented).
     *
     * Must be O(log n) for best and average cases and O(n) for worst case.
     *
     * @param data the data to add
     * @throws java.lang.IllegalArgumentException if data is null
     */
    public void add(T data) {
        root = addHelper(root, data);
    }

    /**
     *
     * @param curr the current node
     * @param data the data to add
     * @return the updated node
     */

    private BSTNode<T> addHelper(BSTNode<T> curr, T data) {
        if (data == null) {
            throw new IllegalArgumentException("Invalid input");
        }
        if (curr == null) {
            curr = new BSTNode<>(data);
            size++;
            return curr;
        }
        int compared = data.compareTo(curr.getData());
        if (compared < 0) {
            curr.setLeft(addHelper(curr.getLeft(), data));
        } else if (compared > 0) {
            curr.setRight(addHelper(curr.getRight(), data));
        }
        return curr;
    }
    /**
     * Removes and returns the data from the tree matching the given parameter.
     *
     * This must be done recursively.
     *
     * There are 3 cases to consider:
     * 1: The node containing the data is a leaf (no children). In this case,
     * simply remove it.
     * 2: The node containing the data has one child. In this case, simply
     * replace it with its child.
     * 3: The node containing the data has 2 children. Use the predecessor to
     * replace the data. You MUST use recursion to find and remove the
     * predecessor (you will likely need an additional helper method to
     * handle this case efficiently).
     *
     * Do not return the same data that was passed in. Return the data that
     * was stored in the tree.
     *
     * Hint: Should you use value equality or reference equality?
     *
     * Must be O(log n) for best and average cases and O(n) for worst case.
     *
     * @param data the data to remove
     * @return the data that was removed
     * @throws java.lang.IllegalArgumentException if data is null
     * @throws java.util.NoSuchElementException   if the data is not in the tree
     */
    public T remove(T data) {
        if (data == null) {
            throw new IllegalArgumentException("Invalid input");
        }
        BSTNode<T> dummy = new BSTNode<>(null);
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
    private BSTNode<T> removeHelper(BSTNode<T> curr, T data, BSTNode<T> dummy) {
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
                BSTNode<T> dummy2 = new BSTNode<>(null);
                curr.setLeft(removePredecessor(curr.getLeft(), dummy2));
                curr.setData(dummy2.getData());
            }
        }
        return curr;
    }
    /**
     *
     * @param curr the current node
     * @param dummy the dummy to store the predecessor
     * @return the updated node
     */
    private BSTNode<T> removePredecessor(BSTNode<T> curr, BSTNode<T> dummy) {
        if (curr.getRight() == null) {
            dummy.setData(curr.getData());
            return curr.getLeft();
        } else {
            curr.setRight(removePredecessor(curr.getRight(), dummy));
        }
        return curr;
    }
    /**
     * Returns the data from the tree matching the given parameter.
     *
     * This must be done recursively.
     *
     * Do not return the same data that was passed in. Return the data that
     * was stored in the tree.
     *
     * Hint: Should you use value equality or reference equality?
     *
     * Must be O(log n) for best and average cases and O(n) for worst case.
     *
     * @param data the data to search for
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
    private T getHelper(BSTNode<T> curr, T data) {
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
     * This must be done recursively.
     *
     * Hint: Should you use value equality or reference equality?
     *
     * Must be O(log n) for best and average cases and O(n) for worst case.
     *
     * @param data the data to search for
     * @return true if the parameter is contained within the tree, false
     * otherwise
     * @throws java.lang.IllegalArgumentException if data is null
     */
    public boolean contains(T data) {
        if (data == null) {
            throw new IllegalArgumentException("Invalid input");
        }
        return containHelper(root, data);
    }
    /**
     *
     * @param curr the current node
     * @param data the data to search for
     * @return whether the date is in the tree
     */
    private boolean containHelper(BSTNode<T> curr, T data) {
        if (curr == null) {
            return false;
        }
        int compared = data.compareTo(curr.getData());
        if (compared == 0) {
            return true;
        } else if (compared < 0) {
            return containHelper(curr.getLeft(), data);
        } else {
            return containHelper(curr.getRight(), data);
        }
    }
    /**
     * Generate a pre-order traversal of the tree.
     *
     * This must be done recursively.
     *
     * Must be O(n).
     *
     * @return the preorder traversal of the tree
     */
    public List<T> preorder() {
        List<T> orderlist = new LinkedList<>();
        return preorderHelper(root, orderlist);
    }

    /**
     *
     * @param curr the current node
     * @param orderlist the list containing the order of the tree
     * @return the preorder traversal of the tree
     */
    private List<T> preorderHelper(BSTNode<T> curr, List<T> orderlist) {
        if (curr != null) {
            orderlist.add(curr.getData());
            preorderHelper(curr.getLeft(), orderlist);
            preorderHelper(curr.getRight(), orderlist);
        }
        return orderlist;
    }

    /**
     * Generate an in-order traversal of the tree.
     *
     * This must be done recursively.
     *
     * Must be O(n).
     *
     * @return the inorder traversal of the tree
     */
    public List<T> inorder() {
        List<T> orderlist = new LinkedList<>();
        return inorderHelper(root, orderlist);
    }

    /**
     *
     * @param curr the current node
     * @param orderlist the list containing the order of the tree
     * @return the inorder traversal of the tree
     */
    private List<T> inorderHelper(BSTNode<T> curr, List<T> orderlist) {
        if (curr != null) {
            inorderHelper(curr.getLeft(), orderlist);
            orderlist.add(curr.getData());
            inorderHelper(curr.getRight(), orderlist);
        }
        return orderlist;
    }

    /**
     * Generate a post-order traversal of the tree.
     *
     * This must be done recursively.
     *
     * Must be O(n).
     *
     * @return the postorder traversal of the tree
     */
    public List<T> postorder() {
        List<T> orderlist = new LinkedList<>();
        return postorderHelper(root, orderlist);
    }

    /**
     *
     * @param curr the current node
     * @param orderlist the list containing the order of the tree
     * @return the postorder traversal of the tree
     */
    private List<T> postorderHelper(BSTNode<T> curr, List<T> orderlist) {
        if (curr != null) {
            postorderHelper(curr.getLeft(), orderlist);
            postorderHelper(curr.getRight(), orderlist);
            orderlist.add(curr.getData());
        }
        return orderlist;
    }
    /**
     * Generate a level-order traversal of the tree.
     *
     * This does not need to be done recursively.
     *
     * Hint: You will need to use a queue of nodes. Think about what initial
     * node you should add to the queue and what loop / loop conditions you
     * should use.
     *
     * Must be O(n).
     *
     * @return the level order traversal of the tree
     */
    public List<T> levelorder() {
        List<T> orderl = new LinkedList<>();
        Queue<BSTNode<T>> q = new LinkedList<>();
        if (size == 0) {
            return orderl;
        }
        q.add(root);
        while (!q.isEmpty()) {
            BSTNode<T> node = q.remove();
            orderl.add(node.getData());
            if (node.getLeft() != null) {
                q.add(node.getLeft());
            }
            if (node.getRight() != null) {
                q.add(node.getRight());
            }
        }
        return orderl;
    }

    /**
     * Returns the height of the root of the tree.
     *
     * This must be done recursively.
     *
     * A node's height is defined as max(left.height, right.height) + 1. A
     * leaf node has a height of 0 and a null child has a height of -1.
     *
     * Must be O(n).
     *
     * @return the height of the root of the tree, -1 if the tree is empty
     */
    public int height() {
        return heightHelper(root);
    }

    /**
     *
     * @param curr the current node
     * @return the height of the tree
     */
    private int heightHelper(BSTNode<T> curr) {
        if (curr == null) {
            return -1;
        }
        int left = heightHelper(curr.getLeft());
        int right = heightHelper(curr.getRight());
        return Math.max(left, right) + 1;
    }

    /**
     * Clears the tree.
     *
     * Clears all data and resets the size.
     *
     * Must be O(1).
     */
    public void clear() {
        root = null;
        size = 0;
    }

    /**
     * Generates a list of the max data per level from the top to the bottom
     * of the tree. (Another way to think about this is to get the right most
     * data per level from top to bottom.)
     * 
     * This must be done recursively.
     *
     * This list should contain the last node of each level.
     *
     * If the tree is empty, an empty list should be returned.
     *
     * Ex:
     * Given the following BST composed of Integers
     *      2
     *    /   \
     *   1     4
     *  /     / \
     * 0     3   5
     * getMaxDataPerLevel() should return the list [2, 4, 5] - 2 is the max
     * data of level 0, 4 is the max data of level 1, and 5 is the max data of
     * level 2
     *
     * Ex:
     * Given the following BST composed of Integers
     *               50
     *           /        \
     *         25         75
     *       /    \
     *      12    37
     *     /  \    \
     *   11   15   40
     *  /
     * 10
     * getMaxDataPerLevel() should return the list [50, 75, 37, 40, 10] - 50 is
     * the max data of level 0, 75 is the max data of level 1, 37 is the
     * max data of level 2, etc.
     *
     * Must be O(n).
     *
     * @return the list containing the max data of each level
     */
    public List<T> getMaxDataPerLevel() {
        List<T> maxl = new LinkedList<>();
        return getMaxHelper(root, maxl, 0);
    }

    /**
     *
     * @param curr the current node
     * @param maxl the list containing the max data of each level
     * @param level the level of the tree where curr is at
     * @return maxl
     */
    private List<T> getMaxHelper(BSTNode<T> curr, List<T> maxl, int level) {
        if (curr == null) { 
            return maxl;
        }
        if (maxl.size() == level) {
            maxl.add(curr.getData());
        }
        getMaxHelper(curr.getRight(), maxl, level + 1);
        getMaxHelper(curr.getLeft(), maxl, level + 1);
        return maxl;
    }


    /**
     * Returns the root of the tree.
     *
     * For grading purposes only. You shouldn't need to use this method since
     * you have direct access to the variable.
     *
     * @return the root of the tree
     */
    public BSTNode<T> getRoot() {
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
