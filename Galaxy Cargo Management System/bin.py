from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException


class Bin: # (node of BinCapAVL) actual bin 
    def __init__(self, bin_id, capacity):
        self.ID = bin_id             
        self.capacity = capacity
        self.objects_tree = AVLTree()       # AVL tree to store objects in this bin

    def add_object(self, obj):
        # Add an object to the bin if there's enough capacity.
        if obj.size > self.capacity:
            raise Exception("Not enough capacity to add this object.")
        else:
            # Add the object to the AVL tree
            self.capacity -= obj.size
            self.objects_tree.insert(obj, 'object')
            

    def delete_object(self, object_id):
        """Delete an object from the bin by its ID."""
        # Create a temporary object for deletion (size and color not needed)
        temp_object = Object(object_id, size=0, color=None)
        # Attempt to delete the object from the AVL tree
        obj = self.objects_tree.delete(temp_object, 'object')
        if obj is None:
            raise Exception("Object not found in the bin.")
        self.capacity += obj.size



class BinCapAVL: #(Node of Bin_AVL) will contain AVL tree of all bins with same capacity
    def __init__(self,bins_capacity):
        self.capacity = bins_capacity
        self.bin_avl = AVLTree()
    
    def insert(self, bin_id, bin_capacity):
        if self.capacity != bin_capacity:
            raise Exception("incorrect binavl --- different bin capacity")
        self.bin_avl.insert()
        
        
