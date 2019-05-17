import networkx as nx
import matplotlib.pyplot as plt

input_logic = ""
errors = False
variables = []


def check_parenthesis(expr):
    stack = []
    global errors
    for i in range(len(expr)):
        if expr[i] == '(':
            stack.append(i)
        else:
            if expr[i] == ')':
                if len(stack) == 0:
                    errors = True
                    return False
                if stack[len(stack) - 1] == 0 and i == len(expr) - 1:
                    return True
                stack.pop()
    if len(stack) != 0:
        errors = True
    return False


def find_operator(expr, operator_type):
    """operator_type:
        1 - NOT
        2 - OR
        3 - XOR
        4 - AND"""

    if operator_type == 1:
        if expr[0] == '!':
            return 0
        else:
            return -1

    parenthesis_count = 0

    for i in range(len(expr) - 1, 0, -1):
        if expr[i] == ')':
            parenthesis_count += 1
        else:
            if expr[i] == '(':
                parenthesis_count -= 1
            else:
                if parenthesis_count == 0:
                    if (operator_type == 4 and expr[i] == '&') or (operator_type == 3 and expr[i] == '^') or \
                            (operator_type == 2 and expr[i] == '|'):
                        return i

    return -1


operators = ['!', '|', '^', '&']


def parse(expr):
    global errors

    if len(expr) == 0:
        errors = True
        return ()

    while check_parenthesis(expr):
        expr = expr[1:-1]

    for i in range(2, 5):
        if find_operator(expr, i) != -1:
            return (operators[i - 1], parse(expr[0:find_operator(expr, i)]),
                    parse(expr[find_operator(expr, i) + 1:]))
    if find_operator(expr, 1) != -1:
        return operators[0], parse(expr[1:])

    if errors:
        return ()

    for i in operators:
        if i in expr:
            errors = True
            return ()

    if expr not in variables:
        variables.append(expr)

    return expr


operators_count = [0, 0, 0, 0]
G = nx.Graph()
nodes = []
edges = []
labels = {}


def convert_to_graph(parse_expr, prev=''):
    if type(parse_expr) == tuple:
        operator = parse_expr[0]
        node_label = operator
        operators_count[operators.index(operator)] += 1
        operator += str(operators_count[operators.index(operator)])

        nodes.append(operator)
        labels[operator] = node_label
        if prev != '':
            edges.append((prev, operator))

        arguments = []
        for i in range(1, len(parse_expr)):
            arguments.append(parse_expr[i])
        for i in arguments:
            convert_to_graph(i, operator)
    else:
        nodes.append(parse_expr)
        labels[parse_expr] = parse_expr
        if prev != '':
            edges.append((prev, parse_expr))


def draw_graph(parse_result):
    convert_to_graph(parse_result)
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    print(G.nodes)
    print(G.edges)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, labels, font_size=16)
    plt.savefig("simple_path.png")
    plt.show()


input_logic = "!(a1&(b|c&(!v)))"
parse_result = parse(input_logic)
draw_graph(parse_result)

input_logic = "a&b|c|(!s&o)"
# print(parse(input_logic))
if errors:
    print("Invalid expression")
