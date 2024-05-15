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

    def test_large_code(self):
        lexer = Lexer("""
            // Initialize variables
            x = 15;
            y = 10;

            // Compute sum
            result = x + y;
            print "The result is: ";
            print result;

            // Conditional statement
            if (result > 20) {
                print "Result is greater than 20.";
            } else {
                print "Result is 20 or less.";
            }
        """)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Verificar que el AST es un Block
        self.assertIsInstance(ast, Block)

        # 1. Verificar asignación: x = 15;
        assign_x = ast.statements[0]
        self.assertIsInstance(assign_x, AssignmentStatement)
        self.assertIsInstance(assign_x.variable, Variable)
        self.assertEqual(assign_x.variable.name, 'x')
        self.assertIsInstance(assign_x.value, Number)
        self.assertEqual(assign_x.value.value, 15)

        # 2. Verificar asignación: y = 10;
        assign_y = ast.statements[1]
        self.assertIsInstance(assign_y, AssignmentStatement)
        self.assertIsInstance(assign_y.variable, Variable)
        self.assertEqual(assign_y.variable.name, 'y')
        self.assertIsInstance(assign_y.value, Number)
        self.assertEqual(assign_y.value.value, 10)

        # 3. Verificar asignación: result = x + y;
        assign_result = ast.statements[2]
        self.assertIsInstance(assign_result, AssignmentStatement)
        self.assertIsInstance(assign_result.variable, Variable)
        self.assertEqual(assign_result.variable.name, 'result')
        self.assertIsInstance(assign_result.value, BinaryOperation)
        self.assertEqual(assign_result.value.operator, '+')
        self.assertIsInstance(assign_result.value.left, Variable)
        self.assertEqual(assign_result.value.left.name, 'x')
        self.assertIsInstance(assign_result.value.right, Variable)
        self.assertEqual(assign_result.value.right.name, 'y')

        # 4. Verificar print "The result is: ";
        print_stmt1 = ast.statements[3]
        self.assertIsInstance(print_stmt1, PrintStatement)
        self.assertIsInstance(print_stmt1.value, String)
        self.assertEqual(print_stmt1.value.value, "The result is: ")

        # 5. Verificar print result;
        print_stmt2 = ast.statements[4]
        self.assertIsInstance(print_stmt2, PrintStatement)
        self.assertIsInstance(print_stmt2.value, Variable)
        self.assertEqual(print_stmt2.value.name, 'result')

        # 6. Verificar if statement
        if_stmt = ast.statements[5]
        self.assertIsInstance(if_stmt, IfStatement)

        # Verificar condición del if: result > 20
        self.assertIsInstance(if_stmt.condition, BinaryOperation)
        self.assertEqual(if_stmt.condition.operator, '>')
        self.assertIsInstance(if_stmt.condition.left, Variable)
        self.assertEqual(if_stmt.condition.left.name, 'result')
        self.assertIsInstance(if_stmt.condition.right, Number)
        self.assertEqual(if_stmt.condition.right.value, 20)

        # Verificar true block: print "Result is greater than 20.";
        self.assertIsInstance(if_stmt.true_block, Block)
        self.assertEqual(len(if_stmt.true_block.statements), 1)
        true_print_stmt = if_stmt.true_block.statements[0]
        self.assertIsInstance(true_print_stmt, PrintStatement)
        self.assertIsInstance(true_print_stmt.value, String)
        self.assertEqual(true_print_stmt.value.value, "Result is greater than 20.")

        # Verificar false block: print "Result is 20 or less.";
        self.assertIsInstance(if_stmt.false_block, Block)
        self.assertEqual(len(if_stmt.false_block.statements), 1)
        false_print_stmt = if_stmt.false_block.statements[0]
        self.assertIsInstance(false_print_stmt, PrintStatement)
        self.assertIsInstance(false_print_stmt.value, String)
        self.assertEqual(false_print_stmt.value.value, "Result is 20 or less.")

    def test_arithmetic_with_parentheses(self):
        lexer = Lexer("3 + (4 * (5 / 2))")
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

        # Verificar el lado derecho de la suma (una multiplicación dentro de paréntesis)
        self.assertIsInstance(main_expr.right, BinaryOperation)
        self.assertEqual(main_expr.right.operator, '*')

        # Verificar el lado izquierdo de la multiplicación
        self.assertIsInstance(main_expr.right.left, Number)
        self.assertEqual(main_expr.right.left.value, 4)

        # Verificar el lado derecho de la multiplicación (una división dentro de paréntesis)
        self.assertIsInstance(main_expr.right.right, BinaryOperation)
        self.assertEqual(main_expr.right.right.operator, '/')
        self.assertIsInstance(main_expr.right.right.left, Number)
        self.assertEqual(main_expr.right.right.left.value, 5)
        self.assertIsInstance(main_expr.right.right.right, Number)
        self.assertEqual(main_expr.right.right.right.value, 2)

    def test_nested_arithmetic_with_parentheses(self):
        lexer = Lexer("((1 + 2) * (3 / 4) - (5 + (6 - 7)))")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Verificar que el AST es un Block
        self.assertIsInstance(ast, Block)
        self.assertEqual(len(ast.statements), 1)

        # Extraer la operación binaria principal
        main_expr = ast.statements[0]

        # Verificar que la operación principal es una resta
        self.assertIsInstance(main_expr, BinaryOperation)
        self.assertEqual(main_expr.operator, '-')

        # Verificar el lado izquierdo de la resta (una multiplicación dentro de paréntesis)
        self.assertIsInstance(main_expr.left, BinaryOperation)
        self.assertEqual(main_expr.left.operator, '*')

        # Verificar la suma dentro de los paréntesis
        self.assertIsInstance(main_expr.left.left, BinaryOperation)
        self.assertEqual(main_expr.left.left.operator, '+')
        self.assertIsInstance(main_expr.left.left.left, Number)
        self.assertEqual(main_expr.left.left.left.value, 1)
        self.assertIsInstance(main_expr.left.left.right, Number)
        self.assertEqual(main_expr.left.left.right.value, 2)

        # Verificar la división dentro de los paréntesis
        self.assertIsInstance(main_expr.left.right, BinaryOperation)
        self.assertEqual(main_expr.left.right.operator, '/')
        self.assertIsInstance(main_expr.left.right.left, Number)
        self.assertEqual(main_expr.left.right.left.value, 3)
        self.assertIsInstance(main_expr.left.right.right, Number)
        self.assertEqual(main_expr.left.right.right.value, 4)

        # Verificar el lado derecho de la resta (una suma dentro de paréntesis)
        self.assertIsInstance(main_expr.right, BinaryOperation)
        self.assertEqual(main_expr.right.operator, '+')
        self.assertIsInstance(main_expr.right.left, Number)
        self.assertEqual(main_expr.right.left.value, 5)

        # Verificar la resta dentro de los paréntesis
        self.assertIsInstance(main_expr.right.right, BinaryOperation)
        self.assertEqual(main_expr.right.right.operator, '-')
        self.assertIsInstance(main_expr.right.right.left, Number)
        self.assertEqual(main_expr.right.right.left.value, 6)
        self.assertIsInstance(main_expr.right.right.right, Number)
        self.assertEqual(main_expr.right.right.right.value, 7)

    def test_variable_assignment_with_parentheses(self):
        lexer = Lexer("x = (1 + (2 * (3 - 4)));")
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

        # Verificar que el valor asignado es una expresión binaria
        self.assertIsInstance(assignment_stmt.value, BinaryOperation)
        self.assertEqual(assignment_stmt.value.operator, '+')

        # Verificar los operandos de la suma
        self.assertIsInstance(assignment_stmt.value.left, Number)
        self.assertEqual(assignment_stmt.value.left.value, 1)

        # Verificar el lado derecho de la suma (una multiplicación dentro de paréntesis)
        self.assertIsInstance(assignment_stmt.value.right, BinaryOperation)
        self.assertEqual(assignment_stmt.value.right.operator, '*')
        self.assertIsInstance(assignment_stmt.value.right.left, Number)
        self.assertEqual(assignment_stmt.value.right.left.value, 2)

        # Verificar la resta dentro de los paréntesis
        self.assertIsInstance(assignment_stmt.value.right.right, BinaryOperation)
        self.assertEqual(assignment_stmt.value.right.right.operator, '-')
        self.assertIsInstance(assignment_stmt.value.right.right.left, Number)
        self.assertEqual(assignment_stmt.value.right.right.left.value, 3)
        self.assertIsInstance(assignment_stmt.value.right.right.right, Number)
        self.assertEqual(assignment_stmt.value.right.right.right.value, 4)

    def test_logical_expression(self):
        lexer = Lexer("1 < 2 && 3 > 2 || 4 == 4")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Verificar que el AST es un Block
        self.assertIsInstance(ast, Block)
        self.assertEqual(len(ast.statements), 1)

        # Extraer la operación lógica principal
        main_expr = ast.statements[0]

        # Verificar que la operación principal es una disyunción (||)
        self.assertIsInstance(main_expr, BinaryOperation)
        self.assertEqual(main_expr.operator, '||')

        # Verificar el lado izquierdo de la disyunción (una conjunción &&)
        self.assertIsInstance(main_expr.left, BinaryOperation)
        self.assertEqual(main_expr.left.operator, '&&')

        # Verificar las comparaciones dentro de la conjunción
        self.assertIsInstance(main_expr.left.left, BinaryOperation)
        self.assertEqual(main_expr.left.left.operator, '<')
        self.assertIsInstance(main_expr.left.left.left, Number)
        self.assertEqual(main_expr.left.left.left.value, 1)
        self.assertIsInstance(main_expr.left.left.right, Number)
        self.assertEqual(main_expr.left.left.right.value, 2)

        self.assertIsInstance(main_expr.left.right, BinaryOperation)
        self.assertEqual(main_expr.left.right.operator, '>')
        self.assertIsInstance(main_expr.left.right.left, Number)
        self.assertEqual(main_expr.left.right.left.value, 3)
        self.assertIsInstance(main_expr.left.right.right, Number)
        self.assertEqual(main_expr.left.right.right.value, 2)

        # Verificar la comparación en el lado derecho de la disyunción
        self.assertIsInstance(main_expr.right, BinaryOperation)
        self.assertEqual(main_expr.right.operator, '==')
        self.assertIsInstance(main_expr.right.left, Number)
        self.assertEqual(main_expr.right.left.value, 4)
        self.assertIsInstance(main_expr.right.right, Number)
        self.assertEqual(main_expr.right.right.value, 4)

    def test_complex_if_statement_with_logical_operators(self):
        lexer = Lexer("""
            if ((x > 1 && y < 2) || (z >= 3 && w <= 4)) {
                result = 1;
            } else {
                result = 0;
            }
        """)
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
        self.assertEqual(if_stmt.condition.operator, '||')

        # Verificar el lado izquierdo de la condición (una conjunción &&)
        self.assertIsInstance(if_stmt.condition.left, BinaryOperation)
        self.assertEqual(if_stmt.condition.left.operator, '&&')
        self.assertIsInstance(if_stmt.condition.left.left, BinaryOperation)
        self.assertEqual(if_stmt.condition.left.left.operator, '>')
        self.assertIsInstance(if_stmt.condition.left.left.left, Variable)
        self.assertEqual(if_stmt.condition.left.left.left.name, 'x')
        self.assertIsInstance(if_stmt.condition.left.left.right, Number)
        self.assertEqual(if_stmt.condition.left.left.right.value, 1)
        self.assertIsInstance(if_stmt.condition.left.right, BinaryOperation)
        self.assertEqual(if_stmt.condition.left.right.operator, '<')
        self.assertIsInstance(if_stmt.condition.left.right.left, Variable)
        self.assertEqual(if_stmt.condition.left.right.left.name, 'y')
        self.assertIsInstance(if_stmt.condition.left.right.right, Number)
        self.assertEqual(if_stmt.condition.left.right.right.value, 2)

        # Verificar el lado derecho de la condición (una conjunción &&)
        self.assertIsInstance(if_stmt.condition.right, BinaryOperation)
        self.assertEqual(if_stmt.condition.right.operator, '&&')
        self.assertIsInstance(if_stmt.condition.right.left, BinaryOperation)
        self.assertEqual(if_stmt.condition.right.left.operator, '>=')
        self.assertIsInstance(if_stmt.condition.right.left.left, Variable)
        self.assertEqual(if_stmt.condition.right.left.left.name, 'z')
        self.assertIsInstance(if_stmt.condition.right.left.right, Number)
        self.assertEqual(if_stmt.condition.right.left.right.value, 3)
        self.assertIsInstance(if_stmt.condition.right.right, BinaryOperation)
        self.assertEqual(if_stmt.condition.right.right.operator, '<=')
        self.assertIsInstance(if_stmt.condition.right.right.left, Variable)
        self.assertEqual(if_stmt.condition.right.right.left.name, 'w')
        self.assertIsInstance(if_stmt.condition.right.right.right, Number)
        self.assertEqual(if_stmt.condition.right.right.right.value, 4)

        # Verificar el bloque verdadero
        self.assertIsInstance(if_stmt.true_block, Block)
        self.assertEqual(len(if_stmt.true_block.statements), 1)
        true_assignment = if_stmt.true_block.statements[0]
        self.assertIsInstance(true_assignment, AssignmentStatement)
        self.assertIsInstance(true_assignment.variable, Variable)
        self.assertEqual(true_assignment.variable.name, 'result')
        self.assertIsInstance(true_assignment.value, Number)
        self.assertEqual(true_assignment.value.value, 1)

        # Verificar el bloque falso
        self.assertIsInstance(if_stmt.false_block, Block)
        self.assertEqual(len(if_stmt.false_block.statements), 1)
        false_assignment = if_stmt.false_block.statements[0]
        self.assertIsInstance(false_assignment, AssignmentStatement)
        self.assertIsInstance(false_assignment.variable, Variable)
        self.assertEqual(false_assignment.variable.name, 'result')
        self.assertIsInstance(false_assignment.value, Number)
        self.assertEqual(false_assignment.value.value, 0)

    def test_large_code_with_parentheses(self):
        lexer = Lexer("""
            // Initialize variables
            a = (1 + (2 * (3 - 4)));
            b = (5 + (6 / (7 + 8)));

            // Compute complex expression
            result = ((a + b) * (a - b)) / ((a * b) + (a / b));
            print "The complex result is: ";
            print result;

            // Conditional statement
            if ((result > 0) && (result < 100)) {
                print "Result is within expected range.";
            } else {
                print "Result is out of expected range.";
            }
        """)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Verificar que el AST es un Block
        self.assertIsInstance(ast, Block)

        # 1. Verificar asignación: a = (1 + (2 * (3 - 4)));
        assign_a = ast.statements[0]
        self.assertIsInstance(assign_a, AssignmentStatement)
        self.assertIsInstance(assign_a.variable, Variable)
        self.assertEqual(assign_a.variable.name, 'a')
        self.assertIsInstance(assign_a.value, BinaryOperation)
        self.assertEqual(assign_a.value.operator, '+')
        self.assertIsInstance(assign_a.value.left, Number)
        self.assertEqual(assign_a.value.left.value, 1)
        self.assertIsInstance(assign_a.value.right, BinaryOperation)
        self.assertEqual(assign_a.value.right.operator, '*')
        self.assertIsInstance(assign_a.value.right.left, Number)
        self.assertEqual(assign_a.value.right.left.value, 2)
        self.assertIsInstance(assign_a.value.right.right, BinaryOperation)
        self.assertEqual(assign_a.value.right.right.operator, '-')
        self.assertIsInstance(assign_a.value.right.right.left, Number)
        self.assertEqual(assign_a.value.right.right.left.value, 3)
        self.assertIsInstance(assign_a.value.right.right.right, Number)
        self.assertEqual(assign_a.value.right.right.right.value, 4)

        # 2. Verificar asignación: b = (5 + (6 / (7 + 8)));
        assign_b = ast.statements[1]
        self.assertIsInstance(assign_b, AssignmentStatement)
        self.assertIsInstance(assign_b.variable, Variable)
        self.assertEqual(assign_b.variable.name, 'b')
        self.assertIsInstance(assign_b.value, BinaryOperation)
        self.assertEqual(assign_b.value.operator, '+')
        self.assertIsInstance(assign_b.value.left, Number)
        self.assertEqual(assign_b.value.left.value, 5)
        self.assertIsInstance(assign_b.value.right, BinaryOperation)
        self.assertEqual(assign_b.value.right.operator, '/')
        self.assertIsInstance(assign_b.value.right.left, Number)
        self.assertEqual(assign_b.value.right.left.value, 6)
        self.assertIsInstance(assign_b.value.right.right, BinaryOperation)
        self.assertEqual(assign_b.value.right.right.operator, '+')
        self.assertIsInstance(assign_b.value.right.right.left, Number)
        self.assertEqual(assign_b.value.right.right.left.value, 7)
        self.assertIsInstance(assign_b.value.right.right.right, Number)
        self.assertEqual(assign_b.value.right.right.right.value, 8)

        # 3. Verificar asignación: result = ((a + b) * (a - b)) / ((a * b) + (a / b));
        assign_result = ast.statements[2]
        self.assertIsInstance(assign_result, AssignmentStatement)
        self.assertIsInstance(assign_result.variable, Variable)
        self.assertEqual(assign_result.variable.name, 'result')
        self.assertIsInstance(assign_result.value, BinaryOperation)
        self.assertEqual(assign_result.value.operator, '/')

        # Verificar multiplicación dentro de paréntesis
        self.assertIsInstance(assign_result.value.left, BinaryOperation)
        self.assertEqual(assign_result.value.left.operator, '*')
        self.assertIsInstance(assign_result.value.left.left, BinaryOperation)
        self.assertEqual(assign_result.value.left.left.operator, '+')
        self.assertIsInstance(assign_result.value.left.left.left, Variable)
        self.assertEqual(assign_result.value.left.left.left.name, 'a')
        self.assertIsInstance(assign_result.value.left.left.right, Variable)
        self.assertEqual(assign_result.value.left.left.right.name, 'b')
        self.assertIsInstance(assign_result.value.left.right, BinaryOperation)
        self.assertEqual(assign_result.value.left.right.operator, '-')
        self.assertIsInstance(assign_result.value.left.right.left, Variable)
        self.assertEqual(assign_result.value.left.right.left.name, 'a')
        self.assertIsInstance(assign_result.value.left.right.right, Variable)
        self.assertEqual(assign_result.value.left.right.right.name, 'b')

        # Verificar suma dentro de paréntesis
        self.assertIsInstance(assign_result.value.right, BinaryOperation)
        self.assertEqual(assign_result.value.right.operator, '+')
        self.assertIsInstance(assign_result.value.right.left, BinaryOperation)
        self.assertEqual(assign_result.value.right.left.operator, '*')
        self.assertIsInstance(assign_result.value.right.left.left, Variable)
        self.assertEqual(assign_result.value.right.left.left.name, 'a')
        self.assertIsInstance(assign_result.value.right.left.right, Variable)
        self.assertEqual(assign_result.value.right.left.right.name, 'b')
        self.assertIsInstance(assign_result.value.right.right, BinaryOperation)
        self.assertEqual(assign_result.value.right.right.operator, '/')
        self.assertIsInstance(assign_result.value.right.right.left, Variable)
        self.assertEqual(assign_result.value.right.right.left.name, 'a')
        self.assertIsInstance(assign_result.value.right.right.right, Variable)
        self.assertEqual(assign_result.value.right.right.right.name, 'b')

        # 4. Verificar print "The complex result is: ";
        print_stmt1 = ast.statements[3]
        self.assertIsInstance(print_stmt1, PrintStatement)
        self.assertIsInstance(print_stmt1.value, String)
        self.assertEqual(print_stmt1.value.value, "The complex result is: ")

        # 5. Verificar print result;
        print_stmt2 = ast.statements[4]
        self.assertIsInstance(print_stmt2, PrintStatement)
        self.assertIsInstance(print_stmt2.value, Variable)
        self.assertEqual(print_stmt2.value.name, 'result')

        # 6. Verificar if statement
        if_stmt = ast.statements[5]
        self.assertIsInstance(if_stmt, IfStatement)

        # Verificar condición del if: (result > 0) && (result < 100)
        self.assertIsInstance(if_stmt.condition, BinaryOperation)
        self.assertEqual(if_stmt.condition.operator, '&&')

        # Verificar el lado izquierdo de la condición (mayor que)
        self.assertIsInstance(if_stmt.condition.left, BinaryOperation)
        self.assertEqual(if_stmt.condition.left.operator, '>')
        self.assertIsInstance(if_stmt.condition.left.left, Variable)
        self.assertEqual(if_stmt.condition.left.left.name, 'result')
        self.assertIsInstance(if_stmt.condition.left.right, Number)
        self.assertEqual(if_stmt.condition.left.right.value, 0)

        # Verificar el lado derecho de la condición (menor que)
        self.assertIsInstance(if_stmt.condition.right, BinaryOperation)
        self.assertEqual(if_stmt.condition.right.operator, '<')
        self.assertIsInstance(if_stmt.condition.right.left, Variable)
        self.assertEqual(if_stmt.condition.right.left.name, 'result')
        self.assertIsInstance(if_stmt.condition.right.right, Number)
        self.assertEqual(if_stmt.condition.right.right.value, 100)

        # Verificar el bloque verdadero
        self.assertIsInstance(if_stmt.true_block, Block)
        self.assertEqual(len(if_stmt.true_block.statements), 1)
        true_print_stmt = if_stmt.true_block.statements[0]
        self.assertIsInstance(true_print_stmt, PrintStatement)
        self.assertIsInstance(true_print_stmt.value, String)
        self.assertEqual(true_print_stmt.value.value, "Result is within expected range.")

        # Verificar el bloque falso
        self.assertIsInstance(if_stmt.false_block, Block)
        self.assertEqual(len(if_stmt.false_block.statements), 1)
        false_print_stmt = if_stmt.false_block.statements[0]
        self.assertIsInstance(false_print_stmt, PrintStatement)
        self.assertIsInstance(false_print_stmt.value, String)
        self.assertEqual(false_print_stmt.value.value, "Result is out of expected range.")


if __name__ == '__main__':
    unittest.main()
