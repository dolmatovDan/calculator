from ..parser import Parser
import pytest


@pytest.fixture
def par():
    return Parser()


@pytest.mark.parametrize("expr,res", [
    ('5', 5),
    ('100230130913201', 100230130913201),
    ('2+3', 5),
    ('3-4', -1),
    (' 7  +   8    ', 15),
    ('6 * 9', 54),
    ('117*214', 25038),
    ('8 / 4', 2),
    ('25/5', 5),
    ('2^5', 32),
    ('2**5', 32),
    ('-1 + 2', 1)
])
def test_simple_expr_1(par, expr, res):
    assert par.parse_expression(expr) == res


@pytest.mark.parametrize("expr,res", [
    ('-2+3-4+5-6+7-8', -5),
    ('1 +  9   +    2     +      8       -        3         - 7 + 4 + 6 + 5  ', 25),
    ('1*2*3*4*5*6*7*8', 40320),
    ('1 * 2 * 4 * 8 * 16', 1024),
    ('-4*5*6*7', -840),
])
def test_simple_expr_2(par, expr, res):
    assert par.parse_expression(expr) == res


@pytest.mark.parametrize("expr,res", [
    ('2 + 2 * 2', 6),
    ('3 * 4 - 6 * 7 + 8 / 4', -28),
    ('2 * 4 ** 5 * 6', 12288),
    ('1 + 2 * 3 ^ 4 - 81 / 3 ** 2', 154),
    ('1 + 3 + 2 * 5 + 8', 22),
    ('2 * 3 * 4 ^ 6 * 7', 172032),
])
def test_operation_order(par, expr, res):
    assert par.parse_expression(expr) == res


@pytest.mark.parametrize("expr,res", [
    ('(2+2)*2', 8),
    ('(2 * 4) ** (2 * 3)', 262144),
    ('(1 + (1 + (1 + (1 + (1 + (1 + (1 + ((((1)))))))))))', 8),
    ('((((2))) + ((((((3)))))))', 5),
    ('(0 + 0) * 0', 0),
    ('    (   (    2   )  +    ( 2  ) )    *  2    ', 8),
    ('((8 - 2 ^ 2) / 2 + (11 - 25 / 5) / 3) * (1 + 1)', 8),
    ('(-2) ** 4', 16),
    ('(-2) ** 3', -8)
])
def test_braced_expr(par, expr, res):
    assert par.parse_expression(expr) == res


@pytest.mark.parametrize("expr,res", [
    ('-3 * 4', -12),
    ('(-3) * 4', -12),
    ('-(3 * 4)', -12),
    ('-3 * (-4)', 12),
    ('(-3) * (-4)', 12),
    ('-(3 * (-4))', 12),
    ('3 * -4', -12),
    ('-3 * -4', 12),
    ('-(3 * -4)', 12)
])
def test_unary_minus(par, expr, res):
    assert par.parse_expression(expr) == res


@pytest.fixture
def epsilon():
    return 1e-8


@pytest.mark.parametrize("expr,res", [
    ('5 / 2', 2.5),
    ('1 / 3', 1 / 3),
    ('-6 / 8', -6/8),
    ('-6 / (-8)', 6/8),
    ('-6 / -8', 6/8),
    ('1 / 7', 1/7),
    ('1001 / 7 / 11 / 13', 1),
    ('1001 / 7 * 30 / 11 * 2 / 6 / 10 / 13', 1),
])
def test_division(par, epsilon, expr, res):
    assert abs(par.parse_expression(expr) - res) < epsilon


@pytest.mark.parametrize("expr,res", [
    ('0.3', 0.3),
    ('4.0', 4.0),
    ('4.000', 4.0),
    ('4.005', 4.005),
    ('4.000000000000000000000', 4.0),
    ('0.1 + 0.2', 0.3),
    ('0.5 - 0.6', -0.1),
    ('1/3 + 5/11', 1/3 + 5/11),
    ('8/9 - 5/19 + (6/17 - 4/31) * (8/47 + 14/37)', 8/9 - 5/19 + (6/17 - 4/31) * (8/47 + 14/37)),
    ('0.19237552251 + 0.55566311282', 0.19237552251 + 0.55566311282),
    ('4 ^ (1/2)', 2),
    ('9 ** 0.5', 3),
    ('10 ** (1/3)', 10 ** (1/3))
])
def test_float_expr(par, epsilon, expr, res):
    assert abs(par.parse_expression(expr) - res) < epsilon


@pytest.mark.parametrize("expr,res", [
    ('2 ^ 80', 2 ** 80),
    ('10 ^ 154', 1e154),
    ('((3 ^ 2) / 3) ^ (1 * (2 * (3)) * (4 * 5))', float(3 ** 120)),
    ('(-2) ** (99)', -(2 ** 99)),
    ('1 / (10 ** 123)', 1e-123),
    ('(-1) / (10 ** 123)', -1e-123),
    ('10 ^ (-123)', 1e-123)
])
def test_large_small(par, expr, res):
    assert par.parse_expression(expr) == res


@pytest.mark.parametrize("expr", [
    '3 / 0',
    '3 / (-0)',
    '8/9 - 5/19 + (6/17 - 4/31) * (8/0 + 14/37)',
    '0 ^ (-1)',
    '(0 * 3) ^ (-100 / 6)',
    '(-1) ^ (1/2)'
])
def test_math_error(par, expr):
    try:
        par.parse_expression(expr)
        assert False
    except:
        pass


@pytest.mark.parametrize("expr", [
    '0,3',
    '1.000.000',
    '1.111.111',
    "2'000'000",
    'a + 4',
    '7 - 8 + j - 10',
    '(3 * (4 - 6) * (7 + f8)) / 2',
    '(2 * 4) ** (2p * 3)',
    '(4 + 5)(7 + 8)',
    '(2 + 3',
    '2 + 3)',
    '((2 + 3)',
    '(2 + 3))',
    '()',
    '()((()())(())())',
    '(',
    ')',
    '1 + * 2',
    '8 - 9 -** 7',
    '6 = 4',
    '3 /* 4',
    '9 @ 8',
    'abacaba',
    'All your base are belong to us.',
    '你们的所有基地都属于我们。',
    '👏🏴󠁧󠁢󠁳󠁣󠁴󠁿🕵️'
])
def test_bad(par, expr):
    try:
        par.parse_expression(expr)
        assert False
    except:
        pass
