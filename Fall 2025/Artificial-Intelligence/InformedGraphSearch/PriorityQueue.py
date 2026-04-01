import math

# Only works for items that can be keys in dicts:
# integer, float, string, Boolean, or a tuple
class PriorityQueue:
    def __init__(self):
        self.index = dict()  # item -> location in heap
        self.heap = (
            []
        )  # A binary heap of tuples: (priority, item) , smallest priority first

        # Nice stats to print at the end
        self.max_count = 0
        self.total_inserts = 0

    def __len__(self):
        return len(self.heap)


    # Adds an item in the right place in the queue
    # If the item is already in the queue, it just
    # updates its priority
    def push_or_decrease(self, new_priority, item):

        # Is the item already in the queue?
        if item in self.index:
            old_location = self.index[item]
            old_priority = self.heap[old_location][0]

            # Wouldn't move item forward in priority queue
            if new_priority >= old_priority:
                return False

            self.heap[old_location] = (new_priority, item)
            self._siftdown(0, old_location)

        else:
            # Update stats
            self.total_inserts += 1
            if len(self.heap) > self.max_count:
                self.max_count = len(self.heap)

            self.heap.append((new_priority, item))
            self._siftdown(0, len(self.heap) - 1)

        return True

    # Removes and returns (priority, item) tuple in the queue
    # with the lowest priority
    def pop(self):
        if len(self) == 0:
            return (None, None)

        # Note what we are returning
        result = self.heap[0]

        # Remove it from the index
        del self.index[result[1]]

        # Move the last item to the first spot
        self.heap[0] = self.heap[-1]
        del self.heap[-1]
        if len(self.heap) > 0:
            self._siftup(0)


        return result

    # Returns the priority of the item that would
    # be popped, returns math.inf if the queue is empty
    def peek_priority(self):
        if len(self.heap) == 0:
            return math.inf

        return self.heap[0][0]

    def peek_item(self):
        if len(self.heap) == 0:
            return None
        return self.heap[0][1]

    # So you can use the "in" operator
    def __contains__(self, item):
        return item in self.index

    # For stats
    def show_stats(self):
        print(
            f"Priority queue stats: max items:{self.max_count:,d}, total inserts:{self.total_inserts:,d}"
        )

    # Returns all the items as a set
    def items(self):
        return set(self.index.keys())

    # The heap magic stolen from heapq
    # Called by insert_or_decrease
    def _siftdown(self, startpos, pos):
        newitem = self.heap[pos]
        # Follow the path to the root, moving parents down until finding a place
        # newitem fits.
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parent = self.heap[parentpos]
            if newitem < parent:
                self.heap[pos] = parent
                self.index[parent[1]] = pos
                pos = parentpos
                continue
            break
        self.heap[pos] = newitem
        self.index[newitem[1]] = pos
        return pos

    # Called by pop
    def _siftup(self, pos):
        endpos = len(self.heap)
        startpos = pos
        newitem = self.heap[pos]
        # Bubble up the smaller child until hitting a leaf.
        childpos = 2 * pos + 1  # leftmost child position
        while childpos < endpos:
            # Set childpos to index of smaller child.
            rightpos = childpos + 1
            if rightpos < endpos and not self.heap[childpos] < self.heap[rightpos]:
                childpos = rightpos
            # Move the smaller child up
            smaller_child = self.heap[childpos]
            self.heap[pos] = smaller_child
            self.index[smaller_child[1]] = pos

            pos = childpos
            childpos = 2 * pos + 1
        # The leaf at pos is empty now.  Put newitem there, and bubble it up
        # to its final resting place (by sifting its parents down).
        self.heap[pos] = newitem
        self.index[newitem[1]] = pos
        self._siftdown(startpos, pos)

