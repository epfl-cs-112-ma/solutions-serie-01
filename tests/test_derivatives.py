from derivatives import *

def test_tree_to_str() -> None:
    a = leaf("a")
    b = leaf("b")
    x = leaf("x")

    x_plus_a = tree("+", x, a)
    x_plus_b = tree("+", x, b)
    x_times_x = tree("*", x, x)

    assert tree_to_str(x_plus_a) == "((x) + (a))"
    assert tree_to_str(tree("*", x_plus_a, x_plus_b)) == "(((x) + (a)) * ((x) + (b)))"
    assert tree_to_str(tree("+", tree("*", x_times_x, x), tree("*", a, x))) == "((((x) * (x)) * (x)) + ((a) * (x)))"
    assert tree_to_str(tree("/", tree("^", x, a), tree("+", x_times_x, tree("*", b, x)))) == "(((x) ^ (a)) / (((x) * (x)) + ((b) * (x))))"

def test_derivative() -> None:
    # We test the results as strings, as it is more convenient

    a = leaf("a")
    b = leaf("b")
    x = leaf("x")

    x_plus_a = tree("+", x, a)
    x_plus_b = tree("+", x, b)
    x_times_x = tree("*", x, x)

    # a local function to help writing our tests
    def derive_to_str(expr: Tree) -> str:
        return tree_to_str(derivative(expr, 'x'))

    # the \ allows to continue the instruction on the next line

    assert derive_to_str(x_plus_a) \
        == "((1) + (0))"
    assert derive_to_str(tree("*", x_plus_a, x_plus_b)) \
        == "((((1) + (0)) * ((x) + (b))) + (((x) + (a)) * ((1) + (0))))"
    assert derive_to_str(tree("+", tree("*", x_times_x, x), tree("*", a, x))) \
        == "((((((1) * (x)) + ((x) * (1))) * (x)) + (((x) * (x)) * (1))) + (((0) * (x)) + ((a) * (1))))"
    assert derive_to_str(tree("/", tree("^", x, a), tree("+", x_times_x, tree("*", b, x)))) \
        == "((((((a) * (1)) * ((x) ^ ((a) - (1)))) * (((x) * (x)) + ((b) * (x)))) - (((x) ^ (a)) * ((((1) * (x)) + ((x) * (1))) + (((0) * (x)) + ((b) * (1)))))) / ((((x) * (x)) + ((b) * (x))) * (((x) * (x)) + ((b) * (x)))))"
