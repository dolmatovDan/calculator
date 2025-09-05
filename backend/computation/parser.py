import re
from typing import List
import math


class Parser:
    def __init__(self):
        self.tokens = []
        self.current_token = 0

    def parse_expression(self, expression: str) -> float:
        """Parses and computes an arithmetic expression"""
        # Удаляем пробелы
        expression = expression.replace(" ", "").lower()

        self.tokens = self._tokenize(expression)
        self.current_token = 0

        result = self._parse_operations(['+-', '*/', '^', '//'])

        if self.current_token < len(self.tokens):
            raise ValueError(f"Unexpected token: {self.tokens[self.current_token]}")

        return result

    def _tokenize(self, expression: str) -> List[str]:
        """Splits the expression into tokens"""
        pattern = r'(\d+\.?\d*|\.\d+|[+\-*/^()]|//)'
        tokens = re.findall(pattern, expression)
        return tokens

    def _parse_operations(self, operation_levels: List[str]) -> float:
        """
        Recursively parses operations based on priority levels
        operation_levels: list of lines with operators in order of priority (from low to high)
        """
        if not operation_levels:
            return self._parse_factor()

        current_ops = operation_levels[0]
        result = self._parse_operations(operation_levels[1:])

        while (self.current_token < len(self.tokens) and
               self.tokens[self.current_token] in current_ops):

            operator = self.tokens[self.current_token]
            self.current_token += 1

            right_operand = self._parse_operations(operation_levels[1:])

            if operator == '+':
                result += right_operand
            elif operator == '-':
                result -= right_operand
            elif operator == '*':
                result *= right_operand
            elif operator == '/':
                if right_operand == 0:
                    raise ValueError("Div by zero")
                result /= right_operand
            elif operator == '^':
                result **= right_operand
            elif operator == '//':
                if right_operand == 0:
                    raise ValueError("Div by zero")
                result = float(math.floor(result / right_operand))

        return result

    def _parse_factor(self) -> float:
        """Parse (values, parenthesis, minus)"""
        if self.current_token >= len(self.tokens):
            raise ValueError("Unexpected end of expression")

        token = self.tokens[self.current_token]

        if token == '-':
            self.current_token += 1
            return -self._parse_factor()

        if token == '(':
            self.current_token += 1
            result = self._parse_operations(['+-', '*/', '^', '//'])
            if (self.current_token >= len(self.tokens) or
                    self.tokens[self.current_token] != ')'):
                raise ValueError("Closing parenthesis is missing")
            self.current_token += 1
            return result

        if self._is_number(token):
            self.current_token += 1
            return float(token)

        raise ValueError(f"Unexpected token: {token}")

    def _is_number(self, token: str) -> bool:
        """Checking that this is a number"""
        try:
            float(token)
            return True
        except ValueError:
            return False