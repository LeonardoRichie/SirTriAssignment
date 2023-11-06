class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f'{self.value}'

def exp(tokens):
    left = term(tokens)
    while tokens and tokens[0] in ('+', '-'):
        op = tokens.pop(0)
        right = term(tokens)
        left = TreeNode(op, [left, right])
    return left

def term(tokens):
    left = factor(tokens)
    while tokens and tokens[0] in ('*', '/', '%'):
        op = tokens.pop(0)
        right = factor(tokens)
        left = TreeNode(op, [left, right])
    return left

def factor(tokens):
    if tokens[0] == '(':
        tokens.pop(0)
        result = exp(tokens)
        if tokens[0] != ')':
            raise ValueError("Invalid expression")
        tokens.pop(0)
        return result
    else:
        return number(tokens)

def number(tokens):
    num_str = ""
    while tokens and (tokens[0].isdigit() or (num_str == "" and tokens[0] in ('-', '+'))):
        num_str += tokens.pop(0)
    if num_str:
        return TreeNode(int(num_str))
    else:
        raise ValueError("Invalid expression")

def tokenize(expression):
    tokens = []
    for char in expression:
        if char != ' ':
            tokens.append(char)
    return tokens

def calculate(expression):
    tokens = tokenize(expression)
    tree = exp(tokens)
    if tokens:
        raise ValueError("Invalid expression")
    return tree, evaluate_tree(tree)

def evaluate_tree(node):
    if isinstance(node.value, int):
        return node.value
    elif node.value == '+':
        return evaluate_tree(node.children[0]) + evaluate_tree(node.children[1])
    elif node.value == '-':
        return evaluate_tree(node.children[0]) - evaluate_tree(node.children[1])
    elif node.value == '*':
        return evaluate_tree(node.children[0]) * evaluate_tree(node.children[1])
    elif node.value == '/':
        return evaluate_tree(node.children[0]) / evaluate_tree(node.children[1])
    elif node.value == '%':
        return evaluate_tree(node.children[0]) % evaluate_tree(node.children[1])
    else:
        raise ValueError("Invalid operator")

def display_parse_tree(node, level=0):
    print("  " * level + str(node.value))
    for child in node.children:
        display_parse_tree(child, level+1)

if __name__ == "__main__":
    expression = input("Enter an arithmetic expression: ")
    try:
        tree, result = calculate(expression)
        print(f"Parse Tree:")
        display_parse_tree(tree)
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")