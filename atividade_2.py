import random
from graphviz import Digraph

class Node:
    def __init__(self, val):
        self.val, self.left, self.right = val, None, None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, val):
        def _ins(n, v):
            if not n:
                return Node(v)
            if v < n.val:
                n.left = _ins(n.left, v)
            elif v > n.val:
                n.right = _ins(n.right, v)
            return n
        self.root = _ins(self.root, val)

    def search(self, val):
        def _src(n, v):
            if not n:
                return False
            if n.val == v:
                return True
            return _src(n.left, v) if v < n.val else _src(n.right, v)
        return _src(self.root, val)

    def delete(self, val):
        def _min(n):
            while n.left:
                n = n.left
            return n
        def _del(n, v):
            if not n:
                return n
            if v < n.val:
                n.left = _del(n.left, v)
            elif v > n.val:
                n.right = _del(n.right, v)
            else:
                if not n.left:
                    return n.right
                if not n.right:
                    return n.left
                t = _min(n.right)
                n.val = t.val
                n.right = _del(n.right, t.val)
            return n
        self.root = _del(self.root, val)

    def height(self):
        def _h(n):
            return -1 if not n else 1 + max(_h(n.left), _h(n.right))
        return _h(self.root)

    def depth(self, val):
        def _d(n, v, d):
            if not n:
                return -1
            if n.val == v:
                return d
            return _d(n.left, v, d+1) if v < n.val else _d(n.right, v, d+1)
        return _d(self.root, val, 0)

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

vals = [55, 30, 80, 20, 45, 70, 90]
bst = BinarySearchTree()
for v in vals:
    bst.insert(v)
bst.visualize().render('bst_fixed', format='png', view=True)

print("Busca 45:", bst.search(45))
bst.delete(30)
print("Após remover 30:", bst.search(30))
bst.insert(60)
print("Após inserir 60:", bst.search(60))
print("Altura:", bst.height())
print("Profundidade de 45:", bst.depth(45))

nums = random.sample(range(1, 201), 15)
bst_r = BinarySearchTree()
for n in nums:
    bst_r.insert(n)
bst_r.visualize().render('bst_random', format='png', view=True)
print("Números:", nums)
print("Altura da árvore aleatória:", bst_r.height())
