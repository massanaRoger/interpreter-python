class ASTNode:
    pass


class BinaryOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Number(ASTNode):
    def __init__(self, value):
        self.value = value


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name


class AssignmentStatement(ASTNode):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value


class PrintStatement(ASTNode):
    def __init__(self, value):
        self.value = value


class IfStatement(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block


class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements
