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


def parse(expr):
    global errors

    operators = ['!', '|', '^', '&']

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


input_logic = "!(a1&(b|c&(!v)))"
print(parse(input_logic))
input_logic = "a&b|c|(!s&o)"
print(parse(input_logic))
if errors:
    print("Invalid expression")
