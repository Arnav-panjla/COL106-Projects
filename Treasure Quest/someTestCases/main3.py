from straw_hat import StrawHatTreasury
from treasure import Treasure

def advanced_test_case():
    """
    Advanced test case with edge cases and complex scenarios.
    """
    m = 4  # Number of crewmates
    treasury = StrawHatTreasury(m)
    
    treasures = [
        # Regular treasures
        Treasure(id=1, size=10, arrival_time=1),
        Treasure(id=2, size=5, arrival_time=2),
        Treasure(id=3, size=8, arrival_time=3),
        
        # Treasures arriving at the same time
        Treasure(id=4, size=3, arrival_time=5),
        
        # Large treasure
        Treasure(id=7, size=100, arrival_time=6),
        
        # Small treasures arriving in quick succession
        Treasure(id=8, size=1, arrival_time=7),
        Treasure(id=9, size=2, arrival_time=8),
        Treasure(id=10, size=1, arrival_time=9),
        
        # Treasure arriving after a long gap
        Treasure(id=11, size=20, arrival_time=50),
        
        # Another batch of simultaneous arrivals
        Treasure(id=12, size=15, arrival_time=51),
        
        # Very small treasure
        Treasure(id=15, size=1, arrival_time=52),
    ]
    
    for treasure in treasures:
        treasury.add_treasure(treasure)
    
    # First completion time check
    print("First Completion Time Check:")
    completed_treasures = treasury.get_completion_time()
    for treasure in completed_treasures:
        print(f"Treasure ID: {treasure.id}, Size: {treasure.size}, Arrival: {treasure.arrival_time}, Completion: {treasure.completion_time}")
    
    # Add more treasures after the first check
    late_treasures = [
        Treasure(id=16, size=30, arrival_time=100),
        Treasure(id=17, size=25, arrival_time=101),
    ]
    
    for treasure in late_treasures:
        treasury.add_treasure(treasure)
    
    # Second completion time check
    print("\nSecond Completion Time Check:")
    completed_treasures = treasury.get_completion_time()
    for treasure in completed_treasures:
        print(f"Treasure ID: {treasure.id}, Size: {treasure.size}, Arrival: {treasure.arrival_time}, Completion: {treasure.completion_time}")
    
    # Verification
    verify_results(completed_treasures)

def verify_results(completed_treasures):
    print("\nVerification:")
    for treasure in completed_treasures:
        if treasure.completion_time < treasure.arrival_time + treasure.size:
            print(f"Error: Treasure {treasure.id} completed too early!")
        else:
            print(f"Treasure {treasure.id} completion time is valid.")
    
    # Check if treasures are sorted by ID
    if all(completed_treasures[i].id < completed_treasures[i+1].id for i in range(len(completed_treasures)-1)):
        print("Treasures are correctly sorted by ID.")
    else:
        print("Error: Treasures are not sorted by ID!")

def main():
    advanced_test_case()

if __name__ == "__main__":
    main()