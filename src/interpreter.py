from src.ast import Block, PrintStatement, AssignmentStatement, IfStatement, BinaryOperation, Number, String, Variable


class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.environment = {}

    def interpret(self):
        self.visit(self.ast)

    def visit(self, node):
        if isinstance(node, Block):
            self.visit_block(node)
        elif isinstance(node, AssignmentStatement):
            self.visit_assignment(node)
        elif isinstance(node, PrintStatement):
            self.visit_print(node)
        elif isinstance(node, IfStatement):
            self.visit_if(node)
        elif isinstance(node, BinaryOperation):
            return self.visit_binary_operation(node)
        elif isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, Variable):
            return self.environment[node.name]
        else:
            raise Exception(f"Unknown node type: {type(node)}")

    def visit_block(self, block):
        for statement in block.statements:
            self.visit(statement)

    def visit_assignment(self, assignment):
        value = self.visit(assignment.value)
        self.environment[assignment.variable.name] = value

    def visit_print(self, print_stmt):
        value = self.visit(print_stmt.value)
        print(value)

    def visit_if(self, if_stmt):
        condition = self.visit(if_stmt.condition)
        if condition:
            self.visit(if_stmt.true_block)
        elif if_stmt.false_block:
            self.visit(if_stmt.false_block)

    def visit_binary_operation(self, bin_op):
        left = self.visit(bin_op.left)
        right = self.visit(bin_op.right)

        if bin_op.operator == '+':
            return left + right
        elif bin_op.operator == '-':
            return left - right
        elif bin_op.operator == '*':
            return left * right
        elif bin_op.operator == '/':
            return left / right
        elif bin_op.operator == '==':
            return left == right
        elif bin_op.operator == '!=':
            return left != right
        elif bin_op.operator == '<':
            return left < right
        elif bin_op.operator == '>':
            return left > right
        elif bin_op.operator == '<=':
            return left <= right
        elif bin_op.operator == '>=':
            return left >= right
        elif bin_op.operator == '&&':
            return left and right
        elif bin_op.operator == '||':
            return left or right
        else:
            raise Exception(f"Unknown operator: {bin_op.operator}")
