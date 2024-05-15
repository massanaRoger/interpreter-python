import unittest

from src.ast import IfStatement
from src.parser import *
from src.lexer import Lexer


class TestParser(unittest.TestCase):
    def test_basic_arithmetic(self):
        lexer = Lexer("3 + 4 * 5 / 2")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Verificar que el AST es un Block
        self.assertIsInstance(ast, Block)
        self.assertEqual(len(ast.statements), 1)

        # Extraer la operación binaria principal
        main_expr = ast.statements[0]

        # Verificar que la operación principal es una suma
        self.assertIsInstance(main_expr, BinaryOperation)
        self.assertEqual(main_expr.operator, '+')

        # Verificar el lado izquierdo de la suma
        self.assertIsInstance(main_expr.left, Number)
        self.assertEqual(main_expr.left.value, 3)

        # Verificar el lado derecho de la suma (una división)
        self.assertIsInstance(main_expr.right, BinaryOperation)
        self.assertEqual(main_expr.right.operator, '/')

        # Verificar el lado izquierdo de la división (una multiplicación)
        self.assertIsInstance(main_expr.right.left, BinaryOperation)
        self.assertEqual(main_expr.right.left.operator, '*')

        # Verificar los operandos de la multiplicación
        self.assertIsInstance(main_expr.right.left.left, Number)
        self.assertEqual(main_expr.right.left.left.value, 4)

        self.assertIsInstance(main_expr.right.left.right, Number)
        self.assertEqual(main_expr.right.left.right.value, 5)

        # Verificar el lado derecho de la división
        self.assertIsInstance(main_expr.right.right, Number)
        self.assertEqual(main_expr.right.right.value, 2)

    def test_variable_assignment(self):
        lexer = Lexer("x = 1;")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Verificar que el AST es un Block
        self.assertIsInstance(ast, Block)
        self.assertEqual(len(ast.statements), 1)

        # Extraer la declaración de asignación
        assignment_stmt = ast.statements[0]

        # Verificar que la declaración es una asignación
        self.assertIsInstance(assignment_stmt, AssignmentStatement)

        # Verificar que la variable asignada es 'x'
        self.assertIsInstance(assignment_stmt.variable, Variable)
        self.assertEqual(assignment_stmt.variable.name, 'x')

        # Verificar que el valor asignado es 1
        self.assertIsInstance(assignment_stmt.value, Number)
        self.assertEqual(assignment_stmt.value.value, 1)

    def test_if_statement(self):
        lexer = Lexer("if (x > 1) { x = x + 1; } else { x = x - 1; }")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Verificar que el AST es un Block
        self.assertIsInstance(ast, Block)
        self.assertEqual(len(ast.statements), 1)

        # Extraer la declaración if
        if_stmt = ast.statements[0]

        # Verificar que la declaración es una instrucción if
        self.assertIsInstance(if_stmt, IfStatement)

        # Verificar la condición del if
        self.assertIsInstance(if_stmt.condition, BinaryOperation)
        self.assertEqual(if_stmt.condition.operator, '>')
        self.assertIsInstance(if_stmt.condition.left, Variable)
        self.assertEqual(if_stmt.condition.left.name, 'x')
        self.assertIsInstance(if_stmt.condition.right, Number)
        self.assertEqual(if_stmt.condition.right.value, 1)

        # Verificar el bloque verdadero
        self.assertIsInstance(if_stmt.true_block, Block)
        self.assertEqual(len(if_stmt.true_block.statements), 1)
        true_assignment = if_stmt.true_block.statements[0]
        self.assertIsInstance(true_assignment, AssignmentStatement)
        self.assertIsInstance(true_assignment.variable, Variable)
        self.assertEqual(true_assignment.variable.name, 'x')
        self.assertIsInstance(true_assignment.value, BinaryOperation)
        self.assertEqual(true_assignment.value.operator, '+')
        self.assertIsInstance(true_assignment.value.left, Variable)
        self.assertEqual(true_assignment.value.left.name, 'x')
        self.assertIsInstance(true_assignment.value.right, Number)
        self.assertEqual(true_assignment.value.right.value, 1)

        # Verificar el bloque falso
        self.assertIsInstance(if_stmt.false_block, Block)
        self.assertEqual(len(if_stmt.false_block.statements), 1)
        false_assignment = if_stmt.false_block.statements[0]
        self.assertIsInstance(false_assignment, AssignmentStatement)
        self.assertIsInstance(false_assignment.variable, Variable)
        self.assertEqual(false_assignment.variable.name, 'x')
        self.assertIsInstance(false_assignment.value, BinaryOperation)
        self.assertEqual(false_assignment.value.operator, '-')
        self.assertIsInstance(false_assignment.value.left, Variable)
        self.assertEqual(false_assignment.value.left.name, 'x')
        self.assertIsInstance(false_assignment.value.right, Number)
        self.assertEqual(false_assignment.value.right.value, 1)


if __name__ == '__main__':
    unittest.main()
