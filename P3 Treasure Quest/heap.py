class Heap:
    '''
    Class to implement a heap with general comparison function
    '''
    def __init__(self, comparison_function, init_array):
        self.comparison_function = comparison_function
        self.heap = init_array
        self.build_heap()

    def build_heap(self):
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self.downheap(i)

    def insert(self, value):
        self.heap.append(value)
        self.upheap(len(self.heap) - 1)

    def extract(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.downheap(0)
        return min_val

    def top(self):
        return self.heap[0] if self.heap else None

    def upheap(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.comparison_function(self.heap[index], self.heap[parent]):
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def downheap(self, index):
        min_index = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.heap) and self.comparison_function(self.heap[left], self.heap[min_index]):
            min_index = left
        if right < len(self.heap) and self.comparison_function(self.heap[right], self.heap[min_index]):
            min_index = right

        if min_index != index:
            self.heap[index], self.heap[min_index] = self.heap[min_index], self.heap[index]
            self.downheap(min_index)  