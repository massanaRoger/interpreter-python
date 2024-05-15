from src.ast import Block, BinaryOperation, Number, Variable, PrintStatement, AssignmentStatement, IfStatement


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = -1
        self.next_token()

    def next_token(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None  # End of token stream

    def parse(self):
        return self.program()

    def eat(self, token_type):
        if self.current_token is None:
            raise Exception("Unexpected end of input.")
        if self.current_token.type == token_type:
            print(f"Eating: {self.current_token.type}, Value: {self.current_token.value}")  # Debug print
            self.next_token()
        else:
            raise Exception(
                f"Expected token {token_type}, but got {self.current_token.type} at line {self.current_token.line}")

    def program(self):
        nodes = []
        while self.current_token is not None and self.current_token.type != 'EOF':
            print(f"Current Token Type: {self.current_token.type}")
            if self.current_token.type == 'LBRACE':
                self.eat('LBRACE')
            elif self.current_token.type == 'ID':
                nodes.append(self.assignment_statement())
            elif self.current_token.type == 'PRINT':
                nodes.append(self.print_statement())
            elif self.current_token.type == 'IF':
                nodes.append(self.if_statement())
            elif self.current_token.type == 'RBRACE':
                self.eat('RBRACE')
                return Block(nodes)
            else:
                nodes.append(self.comparison())
        return Block(nodes)

    def comparison(self):
        node = self.expression()
        while self.current_token is not None and self.current_token.type == 'COMPARE':
            token = self.current_token
            self.eat('COMPARE')
            node = BinaryOperation(left=node, operator=token.value, right=self.expression())
        return node

    def expression(self):
        node = self.term()
        while self.current_token is not None and self.current_token.type == 'OP' and self.current_token.value in (
                '+', '-'):
            token = self.current_token
            if token.value == '+':
                self.eat('OP')
            elif token.value == '-':
                self.eat('OP')
            node = BinaryOperation(left=node, operator=token.value, right=self.term())
        return node

    def term(self):
        """Parse a term from the list of tokens."""
        node = self.factor()  # Start with the highest precedence function that handles factors (numbers, variables,
        # subexpressions)
        while self.current_token is not None and self.current_token.type == 'OP' and self.current_token.value in (
                '*', '/'):
            token = self.current_token
            if token.value == '*':
                self.eat('OP')  # Advance after recognizing an '*'
            elif token.value == '/':
                self.eat('OP')  # Advance after recognizing a '/'

            # Create a new node in the AST, using the current node and the next factor
            node = BinaryOperation(left=node, operator=token.value, right=self.factor())

        return node

    def factor(self):
        """Handle factors which can be numbers, variables, or expressions in parentheses."""
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return Number(token.value)
        elif token.type == 'ID':
            self.eat('ID')
            return Variable(token.value)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')  # Eat the '('
            node = self.expression()  # Process the subexpression
            self.eat('RPAREN')  # Eat the ')'
            return node
        else:
            raise Exception(f'Unexpected token type: {token.type}')

    def assignment_statement(self):
        var_name = self.current_token.value
        self.eat('ID')
        self.eat('ASSIGN')
        expr = self.expression()
        self.eat('END')
        return AssignmentStatement(Variable(var_name), expr)

    def print_statement(self):
        self.eat('PRINT')
        expr = self.expression()
        self.eat('END')
        return PrintStatement(expr)

    def if_statement(self):
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.comparison()
        self.eat('RPAREN')
        true_block = self.parse()
        false_block = None
        if self.current_token is not None and self.current_token.type == 'ELSE':
            self.eat('ELSE')
            false_block = self.parse()

        return IfStatement(condition, true_block, false_block)
