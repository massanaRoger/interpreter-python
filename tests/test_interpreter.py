import unittest
from io import StringIO
import sys

from src.interpreter import Interpreter
from src.lexer import Lexer
from src.parser import Parser


class TestInterpreter(unittest.TestCase):

    def setUp(self):
        self.held_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        self.output = sys.stdout.getvalue()
        sys.stdout = self.held_stdout

    def test_variable_assignment(self):
        code = "x = 10; y = 20; z = x + y;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter(ast)
        interpreter.interpret()

        self.assertEqual(interpreter.environment['x'], 10)
        self.assertEqual(interpreter.environment['y'], 20)
        self.assertEqual(interpreter.environment['z'], 30)

    def test_arithmetic_operations(self):
        code = "result = (2 + 3) * (5 - 2) / 3;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter(ast)
        interpreter.interpret()

        self.assertEqual(interpreter.environment['result'], 5.0)

    def test_logical_operations(self):
        code = "a = 1; b = 2; c = (a < b) && (b > a); d = (a == b) || (a != b);"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter(ast)
        interpreter.interpret()

        self.assertEqual(interpreter.environment['a'], 1)
        self.assertEqual(interpreter.environment['b'], 2)
        self.assertTrue(interpreter.environment['c'])
        self.assertTrue(interpreter.environment['d'])

    def test_print_statement(self):
        code = 'print "Hello, world!"; x = 10; print x;'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter(ast)
        interpreter.interpret()

        output = sys.stdout.getvalue().strip().split('\n')
        self.assertEqual(output[0], "Hello, world!")
        self.assertEqual(output[1], "10")

    def test_if_statement(self):
        code = """
        x = 10;
        y = 20;
        if (x < y) {
            result = x + y;
            print result;
        } else {
            result = x - y;
            print result;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter(ast)
        interpreter.interpret()

        self.assertEqual(interpreter.environment['x'], 10)
        self.assertEqual(interpreter.environment['y'], 20)
        self.assertEqual(interpreter.environment['result'], 30)
        output = sys.stdout.getvalue().strip().split('\n')
        self.assertEqual(output[0], "30")

    def test_complex_logic(self):
        code = """
        x = 10;
        y = 20;
        if ((x < y) && (x > 5)) {
            result = y - x;
        } else {
            result = y + x;
        }
        print result;
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter(ast)
        interpreter.interpret()

        self.assertEqual(interpreter.environment['x'], 10)
        self.assertEqual(interpreter.environment['y'], 20)
        self.assertEqual(interpreter.environment['result'], 10)
        output = sys.stdout.getvalue().strip().split('\n')
        self.assertEqual(output[0], "10")

if __name__ == "__main__":
    unittest.main()
