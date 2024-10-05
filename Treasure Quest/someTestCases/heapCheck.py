from heap import *

def comprehensive_heap_test():
    def min_compare(a, b):
        return -1 if a < b else 1 if a > b else 0

    print("Comprehensive Heap Test")
    print("=======================")

    # Test 1: Basic min heap operations
    print("\nTest 1: Basic min heap operations")
    min_heap = Heap(min_compare, [4, 2, 8, 1, 5, 3])
    print("Initial heap:", min_heap.heap)
    
    print("Extracting elements:")
    for _ in range(len(min_heap.heap)):
        print(min_heap.extract(), end=" ")
    print("\nHeap after extraction:", min_heap.heap)

    # Test 2: Insert operations
    print("\nTest 2: Insert operations")
    min_heap = Heap(min_compare, [])
    elements = [4, 2, 8, 1, 5, 3]
    print("Inserting elements:", elements)
    for elem in elements:
        min_heap.insert(elem)
        print(f"After inserting {elem}:", min_heap.heap)

    # Test 3: Alternating insert and extract
    print("\nTest 3: Alternating insert and extract")
    min_heap = Heap(min_compare, [4, 2, 8])
    print("Initial heap:", min_heap.heap)
    
    operations = [
        ('insert', 1), ('extract',), ('insert', 5), ('extract',),
        ('insert', 3), ('extract',), ('extract',), ('extract',)
    ]
    
    for op in operations:
        if op[0] == 'insert':
            min_heap.insert(op[1])
            print(f"After inserting {op[1]}:", min_heap.heap)
        else:
            extracted = min_heap.extract()
            print(f"Extracted {extracted}. Heap:", min_heap.heap)

    # Test 4: Edge cases
    print("\nTest 4: Edge cases")
    
    # Empty heap
    empty_heap = Heap(min_compare, [])
    print("Empty heap - top:", empty_heap.top())
    print("Empty heap - extract:", empty_heap.extract())
    
    # Single element heap
    single_heap = Heap(min_compare, [42])
    print("Single element heap - top:", single_heap.top())
    print("Single element heap - extract:", single_heap.extract())
    print("After extraction:", single_heap.heap)

    # Test 5: Large number of elements
    print("\nTest 5: Large number of elements")
    import random
    large_elements = [random.randint(1, 1000) for _ in range(1000)]
    large_heap = Heap(min_compare, large_elements)
    print(f"Heap with 1000 elements - top: {large_heap.top()}")
    print("Extracting all elements...")
    extracted = []
    while large_heap.heap:
        extracted.append(large_heap.extract())
    print(f"First 10 extracted: {extracted[:10]}")
    print(f"Last 10 extracted: {extracted[-10:]}")
    if all(extracted[i] <= extracted[i+1] for i in range(len(extracted)-1)):
        print("All elements extracted in correct order")
    else:
        print("Error: Elements not extracted in correct order")

comprehensive_heap_test()