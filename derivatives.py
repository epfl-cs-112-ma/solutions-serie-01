from dataclasses import dataclass

type TreeOpt = Tree | None
"""Optional sub-tree"""

@dataclass(frozen=True)
class Tree:
    """Binary tree, with the representation in the statement."""
    value: str
    left: TreeOpt
    right: TreeOpt

def tree(value: str, left: TreeOpt, right: TreeOpt) -> Tree:
    # Yes, that's all there is to it
    return Tree(value, left, right)

def leaf(value: str) -> Tree:
    return Tree(value, None, None)

def tree_to_str(tree: Tree) -> str:
    if tree.left is None or tree.right is None:
        return f"({tree.value})"
    else:
        left_str = tree_to_str(tree.left)
        right_str = tree_to_str(tree.right)
        return f"({left_str} {tree.value} {right_str})"

def derivative(expr: Tree, x: str) -> Tree:
    """Computes the formal derivative of the given expression."""
    def d(f: Tree) -> Tree:
        return derivative(f, x)

    match expr:
        case Tree(v, None, None) if v == x:
            return leaf('1')
        case Tree(_, None, None):
            return leaf('0')

        case Tree('+', Tree() as f, Tree() as g):
            return tree('+', d(f), d(g))

        case Tree('-', Tree() as f, Tree() as g):
            return tree('-', d(f), d(g))

        case Tree('*', Tree() as f, Tree() as g):
            return tree('+', tree('*', d(f), g), tree('*', f, d(g)))

        case Tree('/', Tree() as f, Tree() as g):
            return tree('/', tree('-', tree('*', d(f), g), tree('*', f, d(g))), tree('*', g, g))

        case Tree('^', Tree() as f, Tree() as g):
            # We assume here that g = a independent of x, as per the statement
            a = g
            return tree('*', tree('*', a, d(f)), tree('^', f, tree('-', a, leaf('1'))))

        case _:
            raise ValueError(f"Invalid tree {expr}")
