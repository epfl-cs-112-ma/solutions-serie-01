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
    if expr.left is None or expr.right is None:
        if expr.value == x:
            return leaf('1')
        else:
            return leaf('0')
    else:
        f = expr.left
        g = expr.right
        df = derivative(f, x)
        dg = derivative(g, x)
        match expr.value:
            case '+':
                return tree('+', df, dg)
            case '-':
                return tree('-', df, dg)
            case '*':
                return tree('+', tree('*', df, g), tree('*', f, dg))
            case '/':
                return tree('/', tree('-', tree('*', df, g), tree('*', f, dg)), tree('*', g, g))
            case '^':
                # We assume here that g = a independent of x, as per the statement
                a = g
                return tree('*', tree('*', a, df), tree('^', f, tree('-', a, leaf('1'))))
            case _:
                raise ValueError(f"Unknown operator {expr.value}")
