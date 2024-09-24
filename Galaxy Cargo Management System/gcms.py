from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException
from node import Node
from bin import Bin, BinCapAVL

class GCMS:
    def __init__(self):
        self.bin_AVL = AVLTree()  # BinAVL tree sorted by capacity
        self.bin_AVL_ID = AVLTree()  # bin tree sorted by ID
        self.object_AVL = AVLTree()

    def add_bin(self, bin_id, capacity):
        new_bin = Bin(bin_id, capacity)
        self.bin_AVL_ID.insert(Node(new_bin, "binID"))

        bin_cap_avl_node = self.bin_AVL.search(Node(BinCapAVL(capacity), "binAVL"))
        if bin_cap_avl_node is None:
            new_bin_cap_avl = BinCapAVL(capacity)
            new_bin_cap_avl.bin_avl.insert(Node(new_bin,"bin_subtree"))
            self.bin_AVL.insert(Node(new_bin_cap_avl, "binAVL"))
        else:
            bin_cap_avl_node.bin_avl.insert(bin_id, capacity)






    def add_object(self, object_id, size, color):
        object_node = Node(Object(object_id, size, color), "objectID")

        if color in [Color.BLUE, Color.YELLOW]:
            bin_cap_avl_node = self.bin_AVL.find_ceiling(Node(BinCapAVL(size), "binAVL"))
        elif color in [Color.RED, Color.GREEN]:
            bin_cap_avl_node = self.bin_AVL.find_max_node()
            print(bin_cap_avl_node.data.bin_avl.inorder_traversal())
        else:
            raise Exception("Invalid color")

        if bin_cap_avl_node is None:
            raise NoBinFoundException("No suitable bin found for the object")

        if color in [Color.BLUE, Color.RED]:
            bin_node = bin_cap_avl_node.data.bin_avl.find_min_node()
            print(l := bin_cap_avl_node.data.bin_avl.inorder_traversal())
        elif color in [Color.YELLOW, Color.GREEN]:
            bin_node = bin_cap_avl_node.data.bin_avl.find_max_node()
        if bin_node is None:
            print("THis is actully none")
        bin_node.data.objects_tree.insert(object_node)
        bin_node.data.capacity-=size # decreasing the size
        bin_cap_avl_node.data.bin_avl.delete(bin_node) # deleting from parent node
        self.add_bin(bin_node.data.ID,bin_node.data.capacity) # adding back to the correct place
        

        # Update bin in bin_AVL_ID
        self.bin_AVL_ID.delete(Node(Bin(bin_node.data.ID, bin_node.data.capacity + size), "binID"))
        self.bin_AVL_ID.insert(Node(bin_node.data, "binID"))

        # Update BinCapAVL
        # if bin.capacity == 0:
        #     bin_cap_avl_node.data.bin_avl.delete(bin_node)
        #     if bin_cap_avl_node.data.bin_avl.size == 0:
        #         self.bin_AVL.delete(bin_cap_avl_node)
        # else:
        #     # Move bin to correct BinCapAVL if capacity changed
        #     old_capacity = bin.capacity + size
        #     if old_capacity != bin.capacity:
        #         bin_cap_avl_node.data.bin_avl.delete(bin_node)
        #         new_bin_cap_avl_node = self.bin_AVL.search(Node(BinCapAVL(bin.capacity), "binAVL"))
        #         if new_bin_cap_avl_node is None:
        #             new_bin_cap_avl = BinCapAVL(bin.capacity)
        #             new_bin_cap_avl.insert(bin.ID, bin.capacity)
        #             self.bin_AVL.insert(Node(new_bin_cap_avl, "binAVL"))
        #         else:
        #             new_bin_cap_avl_node.data.insert(bin.ID, bin.capacity)

        # Add object to object_AVL
        object_node.data.storedBinID = bin_node.data.ID
        self.object_AVL.insert(object_node)






    def delete_object(self, object_id):
        object_node = self.object_AVL.search(Node(Object(object_id, 0, Color.RED), "objectID"))
        if object_node is None:
            return  # Object not found

        bin_node = self.bin_AVL_ID.search(Node(Bin(object_node.data.storedBinID, 0), "binID"))
        if bin_node is None:
            return  # Bin not found

        bin = bin_node.data
        old_capacity = bin.capacity
        bin.delete_object(object_id)

        # Update bin in bin_AVL_ID
        self.bin_AVL_ID.delete(Node(Bin(bin.ID, old_capacity), "binID"))
        self.bin_AVL_ID.insert(Node(bin, "binID"))

        # Update BinCapAVL
        old_bin_cap_avl_node = self.bin_AVL.search(Node(BinCapAVL(old_capacity), "binAVL"))
        old_bin_cap_avl_node.data.bin_avl.delete(Node(bin, "bin"))
        if old_bin_cap_avl_node.data.bin_avl.size == 0:
            self.bin_AVL.delete(old_bin_cap_avl_node)

        new_bin_cap_avl_node = self.bin_AVL.search(Node(BinCapAVL(bin.capacity), "binAVL"))
        if new_bin_cap_avl_node is None:
            new_bin_cap_avl = BinCapAVL(bin.capacity)
            new_bin_cap_avl.insert(bin.ID, bin.capacity)
            self.bin_AVL.insert(Node(new_bin_cap_avl, "binAVL"))
        else:
            new_bin_cap_avl_node.data.insert(bin.ID, bin.capacity)

        # Remove object from object_AVL
        self.object_AVL.delete(object_node)

    def bin_info(self, bin_id):
        bin_node = self.bin_AVL_ID.search(Node(Bin(bin_id, 0), "binID"))
        if bin_node is None:
            return None  # Bin not found
        bin = bin_node.data
        return (bin.capacity, [obj.data.ID for obj in bin.objects_tree.inorder_traversal()])

    def object_info(self, object_id):
        object_node = self.object_AVL.search(Node(Object(object_id, 0, Color.RED), "objectID"))
        if object_node is None:
            return None  # Object not found
        return object_node.data.storedBinID