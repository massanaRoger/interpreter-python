from src.ast import Block, PrintStatement, AssignmentStatement, IfStatement, BinaryOperation, Number, String, Variable
from src.lexer import Lexer
from src.parser import Parser


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


# Example usage
if __name__ == "__main__":
    # This is a placeholder. You should replace it with the actual parsing process.
    code = """
    x = 15;
    y = 10;
    result = x + y;
    print "The result is: ";
    print result;
    if (result > 20) {
        print "Result is greater than 20.";
    } else {
        print "Result is 20 or less.";
    }
    """

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter(ast)
    interpreter.interpret()
