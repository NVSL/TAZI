import ast

tree = ast.parse('block.py')
lines = [None] + code.splitlines()  # None at [0] so we can index lines from 1
test_namespace = {}

for node in tree.body:
    wrapper = ast.Module(body=[node])
    try:
        co = compile(wrapper, "<ast>", 'exec')
        exec(co, test_namespace)
    except AssertionError:
        print("Assertion failed on line", node.lineno, ":")
        print(lines[node.lineno])
        # If the error has a message, show it.
        if e.args:
            print(e)
        print()
