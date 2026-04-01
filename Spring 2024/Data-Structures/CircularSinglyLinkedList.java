import java.util.NoSuchElementException;

/**
 * Your implementation of a CircularSinglyLinkedList without a tail pointer.
 *
 * @author Jinseo Lee
 * @version 1.0
 * @userid jlee4223
 * @GTID 903950086
 *
 * Collaborators: LIST ALL COLLABORATORS YOU WORKED WITH HERE
 *
 * Resources: LIST ALL NON-COURSE RESOURCES YOU CONSULTED HERE
 * TA Office hour
 */
public class CircularSinglyLinkedList<T> {

    /*
     * Do not add new instance variables or modify existing ones.
     */
    private CircularSinglyLinkedListNode<T> head;
    private int size;

    /*
     * Do not add a constructor.
     */

    /**
     * Adds the data to the specified index.
     *
     * Must be O(1) for indices 0 and size and O(n) for all other cases.
     *
     * @param index the index at which to add the new data
     * @param data  the data to add at the specified index
     * @throws java.lang.IndexOutOfBoundsException if index < 0 or index > size
     * @throws java.lang.IllegalArgumentException  if data is null
     */
    public void addAtIndex(int index, T data) {
        if (index < 0 || index > size) {
            throw new IndexOutOfBoundsException("Index out of bounds");
        }
        if (data == null) {
            throw new IllegalArgumentException("Please put in the valid input");
        }
        //edge case1: if adding to the front -> O(1)
        if (index == 0) {
            addToFront(data);
        } else if (index == size) {
            addToBack(data);
        } else {
            CircularSinglyLinkedListNode<T> newNode = new CircularSinglyLinkedListNode<T>(data);
            //traverse till index - 1
            CircularSinglyLinkedListNode<T> curr = head;
            for (int i = 0; i < index - 1; i++) {
                curr = curr.getNext();
            }
            //Node insertion
            newNode.setNext(curr.getNext());
            curr.setNext(newNode);
            size++;
        }
    }

    /**
     * Adds the data to the front of the list.
     *
     * Must be O(1).
     *
     * @param data the data to add to the front of the list
     * @throws java.lang.IllegalArgumentException if data is null
     */
    public void addToFront(T data) {
        if (data == null) {
            throw new IllegalArgumentException("Please put in the valid input");
        }
        //edge case1: when it's the empty list -> set data as head & head.next = head
        if (isEmpty()) {
            head = new CircularSinglyLinkedListNode<T>(data);
            head.setNext(head);
        } else {
            CircularSinglyLinkedListNode<T> newNode = new CircularSinglyLinkedListNode<T>(head.getData());
            //change the original first element to the new data
            head.setData(data);
            //connecting the links
            newNode.setNext(head.getNext());
            head.setNext(newNode);
        }
        size++;
    }

    /**
     * Adds the data to the back of the list.
     *
     * Must be O(1).
     *
     * @param data the data to add to the back of the list
     * @throws java.lang.IllegalArgumentException if data is null
     */
    public void addToBack(T data) {
        if (data == null) {
            throw new IllegalArgumentException("Please put in the valid input");
        }
        //Make a copy of the first element
        if (isEmpty()) {
            head = new CircularSinglyLinkedListNode<T>(data);
            head.setNext(head);
        } else {
            CircularSinglyLinkedListNode<T> newNode = new CircularSinglyLinkedListNode<T>(head.getData());
            //change the original first element to the new data
            head.setData(data);
            //connecting the links
            newNode.setNext(head.getNext());
            head.setNext(newNode);
            //change the head to the next node
            head = head.getNext();
        }
        size++;
    }

    /**
     * Removes and returns the data at the specified index.
     *
     * Must be O(1) for index 0 and O(n) for all other cases.
     *
     * @param index the index of the data to remove
     * @return the data formerly located at the specified index
     * @throws java.lang.IndexOutOfBoundsException if index < 0 or index >= size
     */
    public T removeAtIndex(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Index out of bounds");
        } else if (index == 0) { //edge case1: if removing the front
            return removeFromFront();
        }
        //traverse till index - 1 -> O(n)
        CircularSinglyLinkedListNode<T> curr = head;
        for (int i = 0; i < index - 1; i++) {
            curr = curr.getNext();
        }
        //removing the element
        T element = curr.getNext().getData();
        curr.setNext(curr.getNext().getNext());
        size--;
        return element;
    }

    /**
     * Removes and returns the first data of the list.
     *
     * Must be O(1).
     *
     * @return the data formerly located at the front of the list
     * @throws java.util.NoSuchElementException if the list is empty
     */
    public T removeFromFront() {
        if (isEmpty()) {
            throw new NoSuchElementException("Empty List");
        }
        //store 'out'
        T element = head.getData();
        //set the first element to its next element
        head.setData(head.getNext().getData());
        head.setNext(head.getNext().getNext());
        //edge case1
        if (size == 1) {
            head = null;
        }
        size--;
        return element;
    }

    /**
     * Removes and returns the last data of the list.
     *
     * Must be O(n).
     *
     * @return the data formerly located at the back of the list
     * @throws java.util.NoSuchElementException if the list is empty
     */
    public T removeFromBack() {
        if (isEmpty()) {
            throw new NoSuchElementException("Empty Linked List");
        }
        //traverse to the node right behind the last node -> O(n)
        CircularSinglyLinkedListNode<T> curr = head;
        for (int i = 0; i < size - 2; i++) {
            curr = curr.getNext();
        }
        //eliminate the last node & keep the data
        T element = curr.getNext().getData();
        curr.setNext(head);
        //edge case1
        if (size == 1) {
            head = null;
        }
        size--;
        return element;
    }

    /**
     * Returns the data at the specified index.
     *
     * Should be O(1) for index 0 and O(n) for all other cases.
     *
     * @param index the index of the data to get
     * @return the data stored at the index in the list
     * @throws java.lang.IndexOutOfBoundsException if index < 0 or index >= size
     */
    public T get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Index out of the bounds");
        }
        CircularSinglyLinkedListNode<T> curr = head;
        for (int i = 0; i < index; i++) {
            curr = curr.getNext();
        }
        return curr.getData();
    }

    /**
     * Returns whether or not the list is empty.
     *
     * Must be O(1).
     *
     * @return true if empty, false otherwise
     */
    public boolean isEmpty() {
        return (size == 0);
    }

    /**
     * Clears the list.
     *
     * Clears all data and resets the size.
     *
     * Must be O(1).
     */
    public void clear() {
        head = null;
        size = 0;
    }

    /**
     * Removes and returns the last copy of the given data from the list.
     *
     * Do not return the same data that was passed in. Return the data that
     * was stored in the list.
     *
     * Must be O(n).
     *
     * @param data the data to be removed from the list
     * @return the data that was removed
     * @throws java.lang.IllegalArgumentException if data is null
     * @throws java.util.NoSuchElementException   if data is not found
     */
    public T removeLastOccurrence(T data) {
        if (data == null) {
            throw new IllegalArgumentException("Please put in the valid input");
        }
        CircularSinglyLinkedListNode<T> curr = head;
        CircularSinglyLinkedListNode<T> cand = null;
        //edge case1
        if (size == 0) {
            throw new NoSuchElementException("No data found");
        } else if (size == 1) {
            if (head.getData().equals(data)) {
                T element = head.getData();
                head = null;
                size--;
                return element;
            } else {
                throw new NoSuchElementException("No data found");
            }
        }
        //traverse through the list -> update the candidate node if it equals the data
        for (int i = 0; i < size - 1; i++) {
            if (curr.getNext().getData().equals(data)) {
                cand = curr;
            }
            curr = curr.getNext();
        }
        //edge case2: if the data is only at the front
        if (cand == null && head.getData().equals(data)) {
            return removeFromFront();
        }
        if (cand == null) {
            throw new NoSuchElementException("Data not found");
        }
        //eliminate the data from the list & return the data
        T element = cand.getNext().getData();
        cand.setNext(cand.getNext().getNext());
        size--;
        return element;
    }

    /**
     * Returns an array representation of the linked list.
     *
     * Must be O(n) for all cases.
     *
     * @return the array of length size holding all of the data (not the
     * nodes) in the list in the same order
     */
    public T[] toArray() {
        T[] arr = (T[]) new Object[size];
        CircularSinglyLinkedListNode<T> curr = head;
        for (int i = 0; i < size; i++) {
            arr[i] = curr.getData();
            curr = curr.getNext();
        }
        return arr;
    }

    /**
     * Returns the head node of the list.
     *
     * For grading purposes only. You shouldn't need to use this method since
     * you have direct access to the variable.
     *
     * @return the node at the head of the list
     */
    public CircularSinglyLinkedListNode<T> getHead() {
        // DO NOT MODIFY!
        return head;
    }

    /**
     * Returns the size of the list.
     *
     * For grading purposes only. You shouldn't need to use this method since
     * you have direct access to the variable.
     *
     * @return the size of the list
     */
    public int size() {
        // DO NOT MODIFY!
        return size;
    }
}
