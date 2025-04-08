from dataclasses import dataclass

type Tree = Leaf | Branch
"""Binary tree, with a new representation."""

@dataclass(frozen=True)
class Leaf:
    value: str

@dataclass(frozen=True)
class Branch:
    """Binary operator."""
    operator: str
    left: Tree
    right: Tree

def tree(value: str, left: Tree, right: Tree) -> Tree:
    return Branch(value, left, right)

def leaf(value: str) -> Tree:
    return Leaf(value)

def tree_to_str(tree: Tree) -> str:
    match tree:
        case Leaf(value):
            return f"({value})"
        case Branch(op, left, right):
            left_str = tree_to_str(left)
            right_str = tree_to_str(right)
            return f"({left_str} {op} {right_str})"

def derivative(expr: Tree, x: str) -> Tree:
    """Computes the formal derivative of the given expression."""
    def d(f: Tree) -> Tree:
        return derivative(f, x)

    match expr:
        case Leaf(v) if v == x:
            return leaf('1')
        case Leaf(_):
            return leaf('0')

        case Branch('+', f, g):
            return tree('+', d(f), d(g))

        case Branch('-', f, g):
            return tree('-', d(f), d(g))

        case Branch('*', f, g):
            return tree('+', tree('*', d(f), g), tree('*', f, d(g)))

        case Branch('/', f, g):
            return tree('/', tree('-', tree('*', d(f), g), tree('*', f, d(g))), tree('*', g, g))

        case Branch('^', f, g):
            # We assume here that g = a independent of x, as per the statement
            a = g
            return tree('*', tree('*', a, d(f)), tree('^', f, tree('-', a, leaf('1'))))

        case Branch(op, _, _):
            raise ValueError(f"Invalid operator {op} of tree {expr}")
