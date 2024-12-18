from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_table = self.table
        self.table_size = get_next_size()
        if self.collision_type == "Chain":
            # Save old items
            old_items = []
            for bucket in old_table:
                for item in bucket:
                    if item is not None:
                        old_items.append(item)
            
            # Create new table and reinsert without triggering rehash
            self.table = [[] for _ in range(self.table_size)]
            for item in old_items:
                slot = self.PAhashfunction(item)
                if item not in self.table[slot]:
                    self.table[slot].append(item)

        
        else:  # Linear or Quadratic probing
            old_items = []
            for item in old_table:
                if item is not None:
                    old_items.append(item)
                    
            self.table = [None] * self.table_size
            for item in old_items:
                slot = self.get_slot(item)
                self.table[slot] = item
            
 
        
    def insert(self, x):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(x)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_table = self.table
        self.table_size = get_next_size()
        
        if self.collision_type == "Chain":
            # Save old key-value pairs
            old_items = []
            for bucket in old_table:
                for item in bucket:
                    if item is not None:
                        old_items.append(item)
            
            self.table = [[] for _ in range(self.table_size)]
            for item in old_items:
                slot = self.PAhashfunction(item[0])
                if item not in self.table[slot]:
                     self.table[slot].append(item)
                
                
        else:  # Linear or Quadratic probing
            old_items = []
            for item in old_table:
                if item is not None:
                    old_items.append(item)
                    
            self.table = [None] * self.table_size
            for item in old_items:
                slot = self.get_slot(item[0])
                self.table[slot] = item
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()