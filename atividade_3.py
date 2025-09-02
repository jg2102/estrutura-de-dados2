from graphviz import Digraph
import random

class Node:
    def __init__(self, val):
        self.val, self.left, self.right = val, None, None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if not self.root:
            self.root = Node(val)
            return
        q = [self.root]
        while q:
            n = q.pop(0)
            if not n.left:
                n.left = Node(val)
                break
            else:
                q.append(n.left)
            if not n.right:
                n.right = Node(val)
                break
            else:
                q.append(n.right)

    def inorder(self):
        def _in(n):
            return [] if not n else _in(n.left) + [n.val] + _in(n.right)
        return _in(self.root)

    def preorder(self):
        def _pre(n):
            return [] if not n else [n.val] + _pre(n.left) + _pre(n.right)
        return _pre(self.root)

    def postorder(self):
        def _post(n):
            return [] if not n else _post(n.left) + _post(n.right) + [n.val]
        return _post(self.root)

    def visualize(self):
        dot = Digraph()
        def _edges(n):
            if n:
                dot.node(str(n.val))
                if n.left:
                    dot.edge(str(n.val), str(n.left.val))
                    _edges(n.left)
                if n.right:
                    dot.edge(str(n.val), str(n.right.val))
                    _edges(n.right)
        _edges(self.root)
        return dot

vals_fixed = [55, 30, 80, 20, 45, 70, 90]
bt_f = BinaryTree()
for v in vals_fixed:
    bt_f.insert(v)
bt_f.visualize().render('binary_tree_fixed', format='png', view=True)
print("Fixos:")
print("Inorder:", bt_f.inorder())
print("Preorder:", bt_f.preorder())
print("Postorder:", bt_f.postorder())

vals_rand = random.sample(range(1, 101), 10)
bt_r = BinaryTree()
for v in vals_rand:
    bt_r.insert(v)
bt_r.visualize().render('binary_tree_random', format='png', view=True)
print("\nRandômicos:", vals_rand)
print("Inorder:", bt_r.inorder())
print("Preorder:", bt_r.preorder())
print("Postorder:", bt_r.postorder())
