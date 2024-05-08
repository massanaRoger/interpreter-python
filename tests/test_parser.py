import unittest
from src.parser import *
from src.lexer import Lexer


class TestParser(unittest.TestCase):
    def test_basic_arithmetic(self):
        lexer = Lexer("3 + 4 * 5 / 2")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Assuming you have an AST that represents the expression correctly,
        # you might check for its structure or evaluate it directly if possible.
        self.assertIsInstance(ast, BinaryOperation)
        self.assertEqual(ast.operator, '+')
        self.assertIsInstance(ast.right, BinaryOperation)
        self.assertEqual(ast.right.operator, '/')

        # And so forth—checking the structure to match the expected AST

    def test_variable_assignment(self):
        lexer = Lexer("x = 1")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertIsInstance(ast, AssignmentStatement)
        self.assertIsInstance(ast.value, Number)
        self.assertEqual(ast.value.value, 1)

    def test_if_statement(self):
        lexer = Lexer("if (x > 1) { x = x + 1; } else { x = x - 1; }")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertIsInstance(ast, IfStatement)
        self.assertIsInstance(ast.true_block, Block)
        self.assertIsInstance(ast.false_block, Block)


if __name__ == '__main__':
    unittest.main()
