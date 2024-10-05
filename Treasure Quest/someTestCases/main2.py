from straw_hat import StrawHatTreasury
from treasure import Treasure
import time

def test_case_1():
    """
    Basic test case with a small number of treasures and crewmates.
    """
    m = 2
    treasury = StrawHatTreasury(m)
    
    treasures = [
        Treasure(id=1, size=5, arrival_time=1),
        Treasure(id=2, size=3, arrival_time=2),
        Treasure(id=3, size=4, arrival_time=3),
        Treasure(id=4, size=2, arrival_time=4),
    ]
    
    for treasure in treasures:
        treasury.add_treasure(treasure)
    
    completed_treasures = treasury.get_completion_time()
    
    print("Test Case 1 Results:")
    for treasure in completed_treasures:
        print(f"Treasure ID: {treasure.id}, Completion Time: {treasure.completion_time}")

def test_case_2():
    """
    Test case with varying treasure sizes and arrival times.
    """
    m = 3
    treasury = StrawHatTreasury(m)
    
    treasures = [
        Treasure(id=1, size=10, arrival_time=1),
        Treasure(id=2, size=5, arrival_time=2),
        Treasure(id=3, size=8, arrival_time=3),
        Treasure(id=4, size=3, arrival_time=4),
        Treasure(id=5, size=7, arrival_time=5),
        Treasure(id=6, size=4, arrival_time=6),
    ]
    
    for treasure in treasures:
        treasury.add_treasure(treasure)
    
    completed_treasures = treasury.get_completion_time()
    
    print("\nTest Case 2 Results:")
    for treasure in completed_treasures:
        print(f"Treasure ID: {treasure.id}, Completion Time: {treasure.completion_time}")

def test_case_3():
    """
    Test case with a large number of treasures and crewmates.
    """
    m = 5
    treasury = StrawHatTreasury(m)
    
    for i in range(1, 101):
        size = (i * 7) % 20 + 1  # Generates sizes between 1 and 20
        arrival_time = i
        treasury.add_treasure(Treasure(id=i, size=size, arrival_time=arrival_time))
    
    completed_treasures = treasury.get_completion_time()
    
    print("\nTest Case 3 Results:")
    print(f"Total treasures processed: {len(completed_treasures)}")
    print(f"Last treasure completion time: {completed_treasures[-1].completion_time}")

def test_case_4():
    """
    Test case with multiple get_completion_time calls.
    """
    m = 3
    treasury = StrawHatTreasury(m)
    
    # Add first batch of treasures
    for i in range(1, 6):
        treasury.add_treasure(Treasure(id=i, size=i*2, arrival_time=i))
    
    print("\nTest Case 4 - First Batch Results:")
    completed_treasures = treasury.get_completion_time()
    for treasure in completed_treasures:
        print(f"Treasure ID: {treasure.id}, Completion Time: {treasure.completion_time}")
    
    # Add second batch of treasures
    for i in range(6, 11):
        treasury.add_treasure(Treasure(id=i, size=(11-i)*2, arrival_time=i))
    
    print("\nTest Case 4 - Second Batch Results:")
    completed_treasures = treasury.get_completion_time()
    for treasure in completed_treasures:
        print(f"Treasure ID: {treasure.id}, Completion Time: {treasure.completion_time}")

def main():
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()

if __name__ == "__main__":
    main()