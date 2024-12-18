from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.table_size = params[-1]
        self.collision_type = collision_type
        if collision_type == "Chain":
            self.z = params[0]
            self.table = [[] for i in range(self.table_size)]

        elif collision_type == "Linear":
            self.z = params[0]
            self.table = [None for i in range(self.table_size)]

        else : # Double 
            self.z = params[0]
            self.z2 = params[1]
            self.c2 = params[2]
            self.table = [None for i in range(self.table_size)]
    
    def get_load(self):
        filledSlots = 0
        if self.collision_type == "Chain":
            for i in self.table:
                filledSlots += len(i)
            return filledSlots/self.table_size
        
        else:
            for i in self.table :
                if i is not None:
                        filledSlots += 1
                else:
                    pass
            return filledSlots/self.table_size

    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass
    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)    
    
    def insert(self, key):
        if self.get_load == 1:
            raise Exception("Table is Full")
        
        if self.find(key):
            return
        
        if self.collision_type == "Chain":
            reqSlot = self.get_slot(key)
            if key not in self.table[reqSlot]:
                self.table[reqSlot].append(key)
            else:
                pass

        elif self.collision_type == "Linear":
            reqSlot = self.PAhashfunction(key)
            originalSlot = reqSlot
            while True:
                if self.table[reqSlot] is None :
                    self.table[reqSlot] = key
                    return
                reqSlot = (reqSlot+1) % self.table_size
                if reqSlot == originalSlot:
                    return 
                            
        else :
            reqSlot = self.get_slot(key)
            self.table[reqSlot] = key
            return
        
    
    def find(self, key):
        if self.collision_type == "Chain":
            reqSlot = self.get_slot(key)
            return key in self.table[reqSlot]
        elif self.collision_type == "Linear":
            reqSlot = self.get_slot(key)
            originalSlot = reqSlot
            while self.table[reqSlot] is not None:
                if self.table[reqSlot] == key :
                    return True
                else:
                    reqSlot = (reqSlot+1)%self.table_size
                if reqSlot == originalSlot:
                    break
            return False
        else: # double hashing
            firstHash = self.PAhashfunction(key)
            secondHash = self.hashFunction_2(key)
            slot = firstHash
            while True:
                if self.table[slot] == key:
                    return True
                else:
                    slot = (slot + secondHash)% self.table_size
                if slot == firstHash:
                    return False

    
    def get_slot(self, key):
        if self.collision_type == "Chain":# chaining
            return self.PAhashfunction(key)
        
        elif self.collision_type == "Linear": # Linear
            slot = self.PAhashfunction(key)
            while self.table is None:
                slot = (slot+1)%self.table_size
            return slot
        
        else:# double hashing
            firstHash = self.PAhashfunction(key)
            secondHash = self.hashFunction_2(key)
            slot = firstHash
            while True:
                if self.table[slot] is None:
                    return slot
                slot = (slot + secondHash)% self.table_size
                if slot == firstHash:
                    raise Exception("Table is full..")
                

    def __str__(self):
        if self.collision_type == "Chain":
            return " | ".join(" ; ".join(str(item) for item in slot) if slot else "<EMPTY>" 
                            for slot in self.table)
        else:
            return " | ".join(str(item) if item is not None else "<EMPTY>" 
                            for item in self.table)

    # some extra methods
    def PAhashfunction(self,key):
        alpList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        hVal = 0
        for i in range(len(key)):
            hVal += ((self.z**(i)) * alpList.index(key[i]))
        return hVal % self.table_size
    
    def hashFunction_2(self,key):
        alpList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        hVal = 0
        for i in range(len(key)):
            hVal += ((self.z2**(i)) * alpList.index(key[i]))
        return (self.c2 - (hVal%self.c2))


class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def insert(self, x):
        # x = (key,val)
        # if self.find(x[0]):
        #     return
        
        if self.get_load == 1:
            raise Exception("Table is Full")
        
        if self.collision_type == "Chain":
            reqSlot = self.get_slot(x[0])
            if x not in self.table[reqSlot]:
                self.table[reqSlot].append(x)


        elif self.collision_type == "Linear":
            reqSlot = self.get_slot(x[0])
            self.table[reqSlot] = x
                            
        else :# double hashing
            reqSlot = self.get_slot(x[0])
            self.table[reqSlot] = x

    
    def find(self, key):
        if self.collision_type == "Chain":# chain
            reqSlot = self.PAhashfunction(key)
            for x in self.table[reqSlot]:
                if x[0] == key:
                    return x[1]
            return None
        
        elif self.collision_type == "Linear":# linear
            reqSlot = self.PAhashfunction(key)
            originalSlot = reqSlot
            while self.table[reqSlot] is not None:
                if self.table[reqSlot][0] == key :
                    return self.table[reqSlot][1]
                else:
                    reqSlot = (reqSlot+1)%self.table_size
                if reqSlot == originalSlot:
                    break
            return None
        
        else: # double hashing
            firstHash = self.PAhashfunction(key)
            secondHash = self.hashFunction_2(key)
            slot = firstHash
            while self.table[slot] is not None:
                if self.table[slot][0] == key:
                    return self.table[slot][1]
                slot = (slot + secondHash) % self.table_size
                if slot == firstHash:
                    break
            return None
            
    
    def get_slot(self, key): 

        if self.collision_type == "Chain":
            return self.PAhashfunction(key)
        
        elif self.collision_type == "Linear":
            slot = self.PAhashfunction(key)
            while self.table[slot] is not None:
                slot = (slot+1)%self.table_size
            return slot
        
        else:# double hashing
            firstHash = self.PAhashfunction(key)
            secondHash = self.hashFunction_2(key)
            slot = firstHash
            while self.table[slot] is not None:
                slot = (slot + secondHash)% self.table_size
                if slot == firstHash:
                    raise Exception("No slot found")
            return slot 
    
    def __str__(self):
        if self.collision_type == "Chain":
            return " | ".join(" ; ".join(f"({k}, {v})" for k, v in slot) if slot else "<EMPTY>" 
                            for slot in self.table)
        else:
            return " | ".join(f"({item[0]}, {item[1]})" if item is not None else "<EMPTY>" 
                            for item in self.table)

     # some extra methods
    def PAhashfunction(self,key):
        alpList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        hVal = 0
        for i in range(len(key)):
            hVal += ((self.z**(i)) * alpList.index(key[i]))
        return hVal % self.table_size
    
    def hashFunction_2(self,key):
        alpList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        hVal = 0
        for i in range(len(key)):
            hVal += ((self.z2**(i)) * alpList.index(key[i]))
        return (self.c2 - (hVal%self.c2))
    