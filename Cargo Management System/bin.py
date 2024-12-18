from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException


class Bin: # (node of BinCapAVL) actual bin 
    def __init__(self, bin_id, capacity):
        self.ID = bin_id             
        self.capacity = capacity
        self.objects_tree = AVLTree()       # AVL tree to store objects in this bin



class BinCapAVL: #(Node of Bin_AVL) will contain AVL tree of all bins with same capacity
    def __init__(self,bins_capacity):
        self.capacity = bins_capacity
        self.bin_avl = AVLTree()

        
