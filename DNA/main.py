import networkx as nx
import matplotlib.pyplot as plt
import sys
from DNA.DNA import generate_output

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


operators = ['!', '|', '^', '&', '⊼']


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


operators_count = [0, 0, 0, 0, 0]
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
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, labels, font_size=16)
    plt.savefig(r"DNA\static\DNA\path1.png")
    plt.clf()
    #plt.show()


def replace_to_nand_logic(expr):
    if type(expr) == tuple:
        operator = expr[0]
        if operator == '!':
            return ('⊼', replace_to_nand_logic(expr[1]), replace_to_nand_logic(expr[1]))
        elif operator == '&':
            first_gate = ('⊼', replace_to_nand_logic(expr[1]), replace_to_nand_logic(expr[2]))
            return ('⊼', first_gate, first_gate)
        elif operator == '|':
            first_gate = ('⊼', replace_to_nand_logic(expr[1]), replace_to_nand_logic(expr[1]))
            second_gate = ('⊼', replace_to_nand_logic(expr[2]), replace_to_nand_logic(expr[2]))
            return ('⊼', first_gate, second_gate)
        else:
            first_gate = ('⊼', replace_to_nand_logic(expr[1]), replace_to_nand_logic(expr[2]))
            second_gate = ('⊼', replace_to_nand_logic(expr[1]), first_gate)
            third_gate = ('⊼', first_gate, replace_to_nand_logic(expr[2]))
            return ('⊼', second_gate, third_gate)
    else:
        return expr


values = {}


def get_input_values():
    for var in variables:
        print("Enter", var, "value:")
        input_val = int(input())
        input_val = (False, True)[input_val == 1]
        values[var] = input_val


def DNA_computing_simulation(expr, values):
    if type(expr) == tuple:
        return generate_output(DNA_computing_simulation(expr[1], values), calculate_output(expr[2], values))
    else:
        return values[expr]


def calculate_output(expr, values):
    if type(expr) == tuple:
        return not (calculate_output(expr[1], values) and calculate_output(expr[2], values))
    else:
        return values[expr]


def check_correctness(input_logic):
    global errors
    errors = False
    logic = parse(input_logic)
    if errors:
        return False
    else:
        var_file = open("var.txt", "w+")
        for i in values:
            var_file.write(i)
        return True


def reset():
    global errors, values, operators_count, G, nodes, edges, labels, variables
    errors = False
    values = {}
    operators_count = [0, 0, 0, 0, 0]
    G.clear()
    nodes.clear()
    edges.clear()
    labels.clear()
    variables.clear()

# if __name__ == 'main':
#     args = str(sys.argv)
#     args = args[1:]
#     reset()
#     if args[0] == '-c':
#         check_correctness(args[1])

#input_logic = "!(a1&(b|c&(!v)))"
#input_logic = "a&b|c|(!s&o)"
input_logic = "a&(b|c)"
logic = parse(input_logic)
print(logic)
print(replace_to_nand_logic(logic))
# #draw_graph(logic)
# get_input_values()
# nand_logic = replace_to_nand_logic(logic)
# print(nand_logic)
# print("res:", calculate_output(nand_logic))
# print("DNA res:", DNA_computing_simulation(nand_logic))