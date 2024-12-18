from node import Node

def comp_1(node1, node2):
    if node1.type != node2.type:
        raise Exception("different node!! can't compare")
        
    if node1.type == "binAVL":
        if node1.data.capacity == node2.data.capacity:
            return 0
        else:
            return -1 if node1.data.capacity < node2.data.capacity else 1
    else:
        if node1.data.ID == node2.data.ID :
            return 0
        else:
            return -1 if node1.data.ID < node2.data.ID else 1

class AVLTree:
    def __init__(self, compare_function=comp_1):
        self.root = None
        self.size = 0
        self.comparator = compare_function

    def height(self, node):
        return node.height if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y

    def insert(self, node):
        self.root = self._insert(self.root, node)
        self.size += 1

    def _insert(self, root, node):
        if not root:
            return node

        comp = self.comparator(node, root)
        if comp < 0:
            root.left = self._insert(root.left, node)
        elif comp > 0:
            root.right = self._insert(root.right, node)
        else:
            return root

        self.update_height(root)

        balance = self.balance_factor(root)

        # Left Left Case
        if balance > 1 and self.comparator(node, root.left) < 0:
            return self.rotate_right(root)

        # Right Right Case
        if balance < -1 and self.comparator(node, root.right) > 0:
            return self.rotate_left(root)

        # Left Right Case
        if balance > 1 and self.comparator(node, root.left) > 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Right Left Case
        if balance < -1 and self.comparator(node, root.right) < 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def delete(self, node):
        self.root = self._delete(self.root, node)
        self.size -= 1

    def _delete(self, root, node):
        if not root:
            return root

        comp = self.comparator(node, root)
        if comp < 0:
            root.left = self._delete(root.left, node)
        elif comp > 0:
            root.right = self._delete(root.right, node)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            temp = self.get_min_value_node(root.right)
            root.data, root.type = temp.data, temp.type
            root.right = self._delete(root.right, temp)

        if root is None:
            return root

        self.update_height(root)

        balance = self.balance_factor(root)

        # Left Left Case
        if balance > 1 and self.balance_factor(root.left) >= 0:
            return self.rotate_right(root)

        # Left Right Case
        if balance > 1 and self.balance_factor(root.left) < 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Right Right Case
        if balance < -1 and self.balance_factor(root.right) <= 0:
            return self.rotate_left(root)

        # Right Left Case
        if balance < -1 and self.balance_factor(root.right) > 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search(self, node):
        return self._search(self.root, node)

    def _search(self, root, node):
        if root is None or self.comparator(node, root) == 0:
            return root

        if self.comparator(node, root) < 0:
            return self._search(root.left, node)

        return self._search(root.right, node)

    def inorder_traversal(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node)
            self._inorder_traversal(node.right, result)

    def find_max_node(self):

        if not self.root:
            return None
        return self._find_max_node(self.root)

    def _find_max_node(self, node):
        while node.right:
            node = node.right
        return node

    def find_min_node(self):

        if not self.root:
            return None
        return self._find_min_node(self.root)

    def _find_min_node(self, node):
        while node.left:
            node = node.left
        return node

    def find_ceiling(self, target_node):

        return self._find_ceiling(self.root, target_node)

    def _find_ceiling(self, node, target_node):
        if not node:
            return None

        comp = self.comparator(target_node, node)

        if comp == 0:
            return node
        elif comp < 0:
            ceiling = self._find_ceiling(node.left, target_node)
            return ceiling if ceiling else node
        else:
            return self._find_ceiling(node.right, target_node)