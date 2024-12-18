from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException
from node import Node
from bin import Bin, BinCapAVL

class GCMS:
    def __init__(self):
        self.bin_AVL = AVLTree()  # BinAVL tree sorted by capacity aka BinCapAVL
        self.bin_AVL_ID = AVLTree()  # bin tree sorted by ID
        self.object_AVL = AVLTree()

    def add_bin(self, bin_id, capacity):
        new_bin = Bin(bin_id, capacity)
        self.bin_AVL_ID.insert(Node(new_bin, "binID"))

        bin_cap_avl_node = self.bin_AVL.search(Node(BinCapAVL(capacity), "binAVL"))

        if bin_cap_avl_node is None:
            new_bin_cap_avl = BinCapAVL(capacity)
            new_bin_cap_avl.bin_avl.insert(Node(new_bin,"binID"))
            self.bin_AVL.insert(Node(new_bin_cap_avl, "binAVL"))
        else:
            bin_cap_avl_node.data.bin_avl.insert(Node(new_bin, "binID"))
        


    def add_object(self, object_id, size, color):

        # if already present
        if self.object_AVL.search(Node(Object(object_id, 0, Color.RED), "objectID")):
            raise NoBinFoundException 


        object_node = Node(Object(object_id, size, color), "objectID")

        if color is Color.BLUE or color is Color.YELLOW:
            bin_cap_avl_node = self.bin_AVL.find_ceiling(Node(BinCapAVL(size), "binAVL"))
        elif color is Color.RED or color is Color.GREEN:
            bin_cap_avl_node = self.bin_AVL.find_max_node()
        else:
            # if different color
            raise NoBinFoundException
        
        if bin_cap_avl_node is None:
            raise NoBinFoundException
        
        if bin_cap_avl_node.data.capacity < size:
            raise NoBinFoundException
        
        if color is Color.BLUE or color is Color.RED:
            bin_node = bin_cap_avl_node.data.bin_avl.find_min_node()
            
        elif color is Color.YELLOW or color is Color.GREEN:
            bin_node = bin_cap_avl_node.data.bin_avl.find_max_node()

        if bin_node is None:
                raise NoBinFoundException
    
       
        bin_node_data = bin_node.data
        bin_node.data.objects_tree.insert(object_node)

        del_bin_node = bin_node
        bin_node_data.capacity = bin_node_data.capacity - size # decreasing the size
        bin_cap_avl_node.data.bin_avl.delete(bin_node) # deleting from parent node
        
        # adding back to the correct place
        bin_cap_avl_node_ = self.bin_AVL.search(Node(BinCapAVL(bin_node_data.capacity), "binAVL"))
        if bin_cap_avl_node_ is None:
            new_bin_cap_avl_ = BinCapAVL(bin_node_data.capacity)
            new_bin_cap_avl_.bin_avl.insert(Node(bin_node.data,"binID"))
            self.bin_AVL.insert(Node(new_bin_cap_avl_, "binAVL"))
        else:
            bin_cap_avl_node_.data.bin_avl.insert(Node(bin_node.data,"binID"))

          
            
        # deleting an empty (without any bins) binCapAVL node
        if bin_cap_avl_node.data.bin_avl.root is None:
            self.bin_AVL.delete(bin_cap_avl_node)

        # Update bin in bin_AVL_ID
        self.bin_AVL_ID.delete(Node(del_bin_node.data, "binID"))

        self.bin_AVL_ID.insert(Node(bin_node.data, "binID"))

        # Add object to object_AVL
        self.object_AVL.insert(Node(Object(object_id, size, color, bin_node.data.ID), "objectID"))


    def delete_object(self, object_id):

        object_node = self.object_AVL.search(Node(Object(object_id, 0, Color.RED), "objectID"))
         
        if object_node is None:
            return  # Object not found
        
        # storing size in size variable, randomly acting otherwise
        size = object_node.data.size

        bin_node = self.bin_AVL_ID.search(Node(Bin(object_node.data.storedBinID, 0), "binID"))
        
        if bin_node is None:
            raise NoBinFoundException  # Bin not found

        old_capacity = bin_node.data.capacity
        bin_node.data.objects_tree.delete(object_node) # delete from bin_node
        self.object_AVL.delete(object_node) # delete from object avl 
        bin_node.data.capacity += size # update the capacity

        # Update BinCapAVL
        old_bin_cap_avl_node = self.bin_AVL.search(Node(BinCapAVL(old_capacity), "binAVL"))
        old_bin_cap_avl_node.data.bin_avl.delete(bin_node)

        if old_bin_cap_avl_node.data.bin_avl.root is None:
            self.bin_AVL.delete(old_bin_cap_avl_node)


        bin_cap_avl_node_ = self.bin_AVL.search(Node(BinCapAVL(bin_node.data.capacity), "binAVL"))

        if bin_cap_avl_node_ is None:
            new_bin_cap_avl_ = BinCapAVL(bin_node.data.capacity)
            new_bin_cap_avl_.bin_avl.insert(Node(bin_node.data,"binID"))
            self.bin_AVL.insert(Node(new_bin_cap_avl_, "binAVL"))
        else:
            bin_cap_avl_node_.data.bin_avl.insert(Node(bin_node.data,"binID"))

        # # Update bin in bin_AVL_ID
        temp_bin_node = Node(bin_node.data,"binID")
        self.bin_AVL_ID.delete(bin_node)

        self.bin_AVL_ID.insert(Node(bin_node.data,"binID"))
        self.bin_AVL_ID.insert(temp_bin_node)
        pass



    def bin_info(self, bin_id):
        bin_node = self.bin_AVL_ID.search(Node(Bin(bin_id, 0), "binID"))

        if bin_node is None:
            return # raise NoBinFoundException
        
        return (bin_node.data.capacity, [obj.data.ID for obj in bin_node.data.objects_tree.inorder_traversal()])

    def object_info(self, object_id):
        object_node = self.object_AVL.search(Node(Object(object_id, 0, Color.RED), "objectID"))
        if object_node is None:
            return  # Object not found
        return object_node.data.storedBinID