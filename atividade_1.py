import random
from graphviz import Digraph

class ExprNode:
    def __init__(self, value, left=None, right=None):
        self.value, self.left, self.right = value, left, right

def parse_expression(tokens):
    stack = []
    for t in tokens:
        if t == ')':
            r, o, l = stack.pop(), stack.pop(), stack.pop()
            stack.pop()
            stack.append(ExprNode(o, l, r))
        elif t in '+-*' or t == '(':
            stack.append(t)
        else:
            stack.append(ExprNode(t))
    return stack[0]

def visualize_expr_tree(node, dot=None):
    if dot is None:
        dot = Digraph()
    nid = str(id(node))
    dot.node(nid, str(node.value))
    if node.left:
        lid = str(id(node.left))
        dot.edge(nid, lid)
        visualize_expr_tree(node.left, dot)
    if node.right:
        rid = str(id(node.right))
        dot.edge(nid, rid)
        visualize_expr_tree(node.right, dot)
    return dot

def generate_random_expr():
    ops = ['+', '-', '*']
    nums = [str(random.randint(1, 20)) for _ in range(3)]
    o1, o2 = random.sample(ops, 2)
    if random.choice([0, 1]):
        return f"( ( {nums[0]} {o1} {nums[1]} ) {o2} {nums[2]} )"
    return f"( {nums[0]} {o1} ( {nums[1]} {o2} {nums[2]} ) )"

expr = "( ( 7 + 3 ) * ( 5 - 2 ) )"
tokens = expr.replace('(', ' ( ').replace(')', ' ) ').split()
root = parse_expression(tokens)
visualize_expr_tree(root).render('expr_tree_fixed', format='png', view=True)

expr_rand = generate_random_expr()
tokens_rand = expr_rand.replace('(', ' ( ').replace(')', ' ) ').split()
root_rand = parse_expression(tokens_rand)
visualize_expr_tree(root_rand).render('expr_tree_random', format='png', view=True)
