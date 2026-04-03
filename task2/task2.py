import random

class MaxHeap:
    # Initialize an empty list
    def __init__(self):
        self.heap = []

    # Helper methods to calculate indices in the array representation
    def parent(self, i):
        return (i - 1) // 2

    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2

    # Append new key to the end of the list
    def insert(self, key):
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    # Restore the max-heap property by repeatedly swapping element with its parent
    def _heapify_up(self, i):
        while i > 0 and self.heap[self.parent(i)] < self.heap[i]:
            self.heap[self.parent(i)], self.heap[i] = self.heap[i], self.heap[self.parent(i)]
            i = self.parent(i)
   
    # Remove and return the root (maximum element)
    def extract_max(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    # Sift the new root down to its correct position
    def _heapify_down(self, i):
        largest = i
        left = self.left(i)
        right = self.right(i)
        if left < len(self.heap) and self.heap[left] > self.heap[largest]:
            largest = left
        if right < len(self.heap) and self.heap[right] > self.heap[largest]:
            largest = right
        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self._heapify_down(largest)

    # Build a max heap from an unsorted array
    def heapify(self, arr):
        self.heap = arr[:]
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._heapify_down(i)

    # Return the root without removing it
    def peek(self):
        return self.heap[0] if self.heap else None

# Function to sort the array in-place in ascending order
def heap_sort(arr):
    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(i, 0)
    return arr

if __name__ == "__main__":
    print("1. MaxHeap Demonstration")

    print("\nA. Insertion")
    heap = MaxHeap()
    values = [random.randint(1, 100) for _ in range(5)]
    print("Original array = []")
    for val in values:
        heap.insert(val)
        print(f"Inserted {val}, updated array = {heap.heap}, peek = {heap.peek()}")

    print("\nB. Max Extraction")
    print("Before extraction:", heap.heap)
    while heap.heap:
        max_val = heap.extract_max()
        print(f"Extracted {max_val}, updated array = {heap.heap}, peek = {heap.peek() if heap.heap else None}")

    print("\nC. Heapify")
    heap2 = MaxHeap()
    original_arr = [random.randint(1, 100) for _ in range(5)]
    print("Original array =", original_arr)
    heap2.heapify(original_arr)
    print("Heapified array =", heap2.heap)
    print("Peek:", heap2.peek())

    print("\n2. Heap Sort Demonstration")
    arr = [random.randint(1, 100) for _ in range(7)]
    print("Original array =", arr)
    sorted_arr = heap_sort(arr.copy())
    print("Sorted array =", sorted_arr)
