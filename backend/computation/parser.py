from lark import Lark, Transformer, v_args
import math


class Parser:
    def __init__(self):
        grammar = r"""
            ?start: expr

            ?expr: expr "+" term   -> add
                 | expr "-" term   -> sub
                 | term

            ?term: term "*" power   -> mul
                 | term "/" power   -> div
                 | term "//" power  -> floordiv
                 | term "%" power   -> mod
                 | power

            ?power: atom "^" power -> pow
                  | atom

            ?atom: NUMBER           -> number
                 | "-" atom         -> neg
                 | "(" expr ")"
                 | NAME             -> var
                 | NAME "(" args ")" -> func

            ?args: expr ("," expr)*

            %import common.CNAME -> NAME
            %import common.NUMBER
            %import common.WS_INLINE
            %ignore WS_INLINE
        """

        @v_args(inline=True)
        class CalcTransformer(Transformer):
            def init(self, outer):
                self.outer = outer

            def number(self, token): return float(token)
            def var(self, name):
                n = str(name)
                if n in self.outer.vars:
                    return self.outer.vars[n]
                raise ValueError(f"Неизвестная переменная: {n}")

            def func(self, name, *args):
                n = str(name)
                if n in self.outer.funcs:
                    return self.outer.funcs[n](*args)
                raise ValueError(f"Неизвестная функция: {n}")

            def add(self, a, b): return a + b
            def sub(self, a, b): return a - b
            def mul(self, a, b): return a * b
            def div(self, a, b):
                if (b == 0):
                    raise ValueError("Div by zero")
                return a / b
            def floordiv(self, a, b):
                if (b == 0):
                    raise ValueError("Div by zero")
                return int(a / b)  # trunc
            def mod(self, a, b):
                if (b == 0):
                    raise ValueError("Div by zero")
                return a - int(a / b) * b  # остаток со знаком делимого
            def pow(self, a, b):
                if (a == 0 and b <= 0):
                    raise ValueError("Div by zero")
                res = a ** b
                if isinstance(res, complex):
                    raise ValueError("sqrt(-1)")
                return res
            def neg(self, a): return -a

        # Константы и функции
        self.vars = {"pi": math.pi, "e": math.e}
        self.funcs = {
            "sqrt": math.sqrt,
            "log": math.log,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "abs": abs,
            "round": round,
            "max": max,
            "min": min,
        }

        self.parser = Lark(grammar, parser="lalr", transformer=CalcTransformer(self))

    def parse_expression(self, expr: str):
        """Парсинг и вычисление выражения"""
        try:
            res = self.parser.parse(expr)
        except Exception as e:
            if isinstance(e, ValueError):
                raise e
            else:
                raise ValueError("unexpected token")

        return self.parser.parse(expr)