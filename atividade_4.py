from graphviz import Digraph
import random

class AVLNode:
    def __init__(self, val):
        self.val, self.left, self.right, self.h = val, None, None, 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, val):
        def _ins(n, v):
            if not n:
                return AVLNode(v)
            if v < n.val:
                n.left = _ins(n.left, v)
            elif v > n.val:
                n.right = _ins(n.right, v)
            else:
                return n
            n.h = 1 + max(self._h(n.left), self._h(n.right))
            b = self._bal(n)
            if b > 1 and v < n.left.val:
                return self._rot_r(n)
            if b < -1 and v > n.right.val:
                return self._rot_l(n)
            if b > 1 and v > n.left.val:
                n.left = self._rot_l(n.left)
                return self._rot_r(n)
            if b < -1 and v < n.right.val:
                n.right = self._rot_r(n.right)
                return self._rot_l(n)
            return n
        self.root = _ins(self.root, val)

    def _h(self, n): return 0 if not n else n.h
    def _bal(self, n): return 0 if not n else self._h(n.left) - self._h(n.right)

    def _rot_l(self, z):
        y, t2 = z.right, z.right.left
        y.left, z.right = z, t2
        z.h = 1 + max(self._h(z.left), self._h(z.right))
        y.h = 1 + max(self._h(y.left), self._h(y.right))
        return y

    def _rot_r(self, z):
        y, t3 = z.left, z.left.right
        y.right, z.left = z, t3
        z.h = 1 + max(self._h(z.left), self._h(z.right))
        y.h = 1 + max(self._h(y.left), self._h(y.right))
        return y

    def visualize(self):
        dot = Digraph()
        def _edges(n):
            if n:
                dot.node(str(n.val), f"{n.val}\n(h={n.h})")
                if n.left:
                    dot.edge(str(n.val), str(n.left.val))
                    _edges(n.left)
                if n.right:
                    dot.edge(str(n.val), str(n.right.val))
                    _edges(n.right)
        _edges(self.root)
        return dot

    def inorder(self):
        def _in(n): return [] if not n else _in(n.left) + [n.val] + _in(n.right)
        return _in(self.root)

    def height(self):
        return self._h(self.root) - 1

print("Rotações Simples:")
avl1 = AVLTree()
for v in [10, 20, 30]:
    avl1.insert(v)
    avl1.visualize().render(f'avl_simple_{v}', format='png', view=True)
    print(f"Inserido {v}: Inorder ->", avl1.inorder())

print("\nRotação Dupla:")
avl2 = AVLTree()
for v in [10, 30, 20]:
    avl2.insert(v)
    avl2.visualize().render(f'avl_double_{v}', format='png', view=True)
    print(f"Inserido {v}: Inorder ->", avl2.inorder())

print("\nAVL Randômica:")
avl_r = AVLTree()
vals = random.sample(range(1, 101), 20)
for v in vals:
    avl_r.insert(v)
avl_r.visualize().render('avl_random', format='png', view=True)
print("Valores:", vals)
print("Inorder:", avl_r.inorder())
print("Altura:", avl_r.height())
