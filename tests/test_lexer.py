import unittest
from src.lexer import Lexer, Token


class TestLexer(unittest.TestCase):
    def test_numbers(self):
        code = "123 456.789"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Token('NUMBER', 123, 1, 0),
            Token('NUMBER', 456.789, 1, 4)
        ])

    def test_identifiers(self):
        code = "x y z123"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Token('ID', 'x', 1, 0),
            Token('ID', 'y', 1, 2),
            Token('ID', 'z123', 1, 4)
        ])

    def test_operators(self):
        code = "+ - * /"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Token('OP', '+', 1, 0),
            Token('OP', '-', 1, 2),
            Token('OP', '*', 1, 4),
            Token('OP', '/', 1, 6)
        ])

    def test_strings(self):
        code = '"Hello, world!" "123"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Token('STRING', '"Hello, world!"', 1, 0),
            Token('STRING', '"123"', 1, 16)
        ])

    def test_comments(self):
        code = "// This is a comment\nx = 10"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Token('ID', 'x', 2, 0),
            Token('ASSIGN', '=', 2, 2),
            Token('NUMBER', 10, 2, 4)
        ])

    def test_structure(self):
        code = "if (x > 10) { print x; }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Token('IF', 'if', 1, 0),
            Token('LPAREN', '(', 1, 3),
            Token('ID', 'x', 1, 4),
            Token('COMPARE', '>', 1, 6),
            Token('NUMBER', 10, 1, 8),
            Token('RPAREN', ')', 1, 10),
            Token('LBRACE', '{', 1, 12),
            Token('PRINT', 'print', 1, 14),
            Token('ID', 'x', 1, 20),
            Token('END', ';', 1, 21),
            Token('RBRACE', '}', 1, 23)
        ])

    def test_logical_operators(self):
        code = "if (x > 1 && y < 2 || z == 3) { print x; }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [
            Token('IF', 'if', 1, 0),
            Token('LPAREN', '(', 1, 3),
            Token('ID', 'x', 1, 4),
            Token('COMPARE', '>', 1, 6),
            Token('NUMBER', 1, 1, 8),
            Token('LOGICAL', '&&', 1, 10),
            Token('ID', 'y', 1, 13),
            Token('COMPARE', '<', 1, 15),
            Token('NUMBER', 2, 1, 17),
            Token('LOGICAL', '||', 1, 19),
            Token('ID', 'z', 1, 22),
            Token('COMPARE', '==', 1, 24),
            Token('NUMBER', 3, 1, 27),
            Token('RPAREN', ')', 1, 28),
            Token('LBRACE', '{', 1, 30),
            Token('PRINT', 'print', 1, 32),
            Token('ID', 'x', 1, 38),
            Token('END', ';', 1, 39),
            Token('RBRACE', '}', 1, 41)
        ])


if __name__ == '__main__':
    unittest.main()
