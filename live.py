# LEXING

from typing import Any

RET = {}
class token():
    typ: str
    val: str

    def __init__(self, typ, val):
        """
        >>> token('sym', '(')
        token('sym', '(')
        """
        self.typ = typ
        self.val = val

    def __repr__(self):
        return f'token({self.typ!r}, {self.val!r})'


def lex(s: str) -> list[token]:
    """
    >>> lex('')
    []
    >>> lex('true false falsehood x')
    [token('kw', 'true'), token('kw', 'false'), token('var', 'falsehood'), token('var', 'x')]
    >>> lex('\\n!\\ra ||\\t b && c')
    [token('sym', '!'), token('var', 'a'), token('sym', '||'), token('var', 'b'), token('sym', '&&'), token('var', 'c')]
    >>> lex('))\\t\\t(   !a')
    [token('sym', ')'), token('sym', ')'), token('sym', '('), token('sym', '!'), token('var', 'a')]
    >>> lex('123 4.56')
    [token('num', '123'), token('num', '4.56')]
    """

    tokens = []
    i = 0

    while i < len(s):
        if s[i].isspace():
            i += 1
        # elif s[i].isalpha():
        #     end = i + 1
        #     while end < len(s) and (s[end].isalnum() or s[end] == '_'):
        #         end += 1
        #     assert end >= len(s) or not (s[end].isalnum() or s[end] == '_')
        #
        #     word = s[i:end]
        #
        #     if word in ['true', 'false']:
        #         tokens.append(token('kw', word))
        #     else:
        #         tokens.append(token('var', word))
        #
        #     i = end

        elif s[i].isdigit():
            end = i + 1
            while end < len(s) and s[end].isdigit():
                end += 1
            if end < len(s) and s[end] == '.':
                end += 1
                while end < len(s) and s[end].isdigit():
                    end += 1
                tokens.append(token('num', s[i:end]))
            else:
                tokens.append(token('num', s[i:end]))
            i = end

        elif s[i].isalpha():
            end = i + 1
            while end < len(s) and s[end].isalnum() or s[end] == '_':
                end += 1
            tokens.append(token('var', s[i:end]))
            i = end

        elif s[i] == '=':
            tokens.append(token('sym', '='))
            i += 1
        elif s[i] == '!':
            tokens.append(token('sym', '!'))
            i += 1
        elif s[i] == '+':
            tokens.append(token('sym', '+'))
            i += 1
        elif s[i] == '-':
            tokens.append(token('sym', '-'))
            i += 1
        elif s[i] == '*':
            tokens.append(token('sym', '*'))
            i += 1
        elif s[i] == '/':
            tokens.append(token('sym', '/'))
            i += 1
        elif s[i] == '%':
            tokens.append(token('sym', '/'))
            i += 1
        elif s[i] == '^':
            tokens.append(token('sym', '^'))
            i += 1
        elif s[i] == '(':
            tokens.append(token('sym', '('))
            i += 1
        elif s[i] == ')':
            tokens.append(token('sym', ')'))
            i += 1
        elif s[i:i + 2] == '||':
            tokens.append(token('sym', '||'))
            i += 2
        elif s[i:i + 2] == '&&':
            tokens.append(token('sym', '&&'))
            i += 2
        else:
            raise SyntaxError(f'unexpected character {s[i]}')

    return tokens


# PARSING

class ast():
    typ: str
    children: tuple[Any, ...]

    def __init__(self, typ: str, *children: Any):
        """
        x || true
        >>> ast('||', ast('var', 'x'), ast('val', True))
        ast('||', ast('var', 'x'), ast('val', True))
        """
        self.typ = typ
        self.children = children

    def __repr__(self):
        return f'ast({self.typ!r}, {", ".join([repr(c) for c in self.children])})'


def parse(s: str) -> ast:
    ts = lex(s)

    # a, i = disj(ts, 0)

    a, i = assign(ts, 0)

    if i != len(ts):
        raise SyntaxError(f"expected EOF, found {ts[i:]!r}")

    return a


def assign(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError('expected assign, found EOF')

    lhs, i = add_sub(ts, i)

    while i < len(ts) and ts[i].typ == 'sym' and ts[i].val == '=':
        flag_as = ts[i].val
        rhs, i = add_sub(ts, i + 1)
        lhs = ast(flag_as, lhs, rhs)

    return lhs, i


def add_sub(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError('expected add_sub, found EOF')

    lhs, i = mult_div_mod(ts, i)

    while i < len(ts) and ts[i].typ == 'sym' and (ts[i].val == '+' or ts[i].val == '-'):
        flag_as = ts[i].val
        rhs, i = mult_div_mod(ts, i + 1)
        lhs = ast(flag_as, lhs, rhs)

    return lhs, i


def mult_div_mod(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError('expected mult_div_mod, found EOF')

    lhs, i = expon(ts, i)

    while i < len(ts) and ts[i].typ == 'sym' and (ts[i].val == '*' or ts[i].val == '/' or ts[i].val == '%'):
        flag_md = ts[i].val
        rhs, i = expon(ts, i + 1)
        lhs = ast(flag_md, lhs, rhs)

    return lhs, i


def expon(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError('expected expon, found EOF')

    lhs, i = atom(ts, i)

    while i < len(ts) and ts[i].typ == 'sym' and ts[i].val == '^':
        flag_md = ts[i].val
        rhs, i = atom(ts, i + 1)
        lhs = ast(flag_md, lhs, rhs)

    return lhs, i


def atom(ts: list[token], i: int) -> tuple[ast, int]:
    t = ts[i]

    if t.typ == 'var':
        return ast('var', t.val), i + 1
    elif t.typ == 'num':
        return ast('num', t.val), i + 1
    elif t.typ == 'kw' and t.val in ['true', 'false']:
        return ast('val', t.val == 'true'), i + 1
    elif t.typ == 'sym' and t.val == '(':
        a, i = add_sub(ts, i + 1)

        if i >= len(ts):
            raise SyntaxError(f'expected right paren, got EOF')

        if not (ts[i].typ == 'sym' and ts[i].val == ')'):
            raise SyntaxError(f'expected right paren, got "{ts[i]}"')
        return a, i + 1

    elif ts[i].val == '-':
        a, i = atom(ts, i + 1)
        return ast('-', a), i

    raise SyntaxError(f'expected atom, got "{ts[i]}"')


# def disj(ts: list[token], i: int) -> tuple[ast, int]:
#     """
#     >>> parse('true || false')
#     ast('||', ast('val', True), ast('val', False))
#     """
#     if i >= len(ts):
#         raise SyntaxError('expected conjunction, found EOF')
#
#     lhs, i = conj(ts, i)
#
#     while i < len(ts) and ts[i].typ == 'sym' and ts[i].val == '||':
#         rhs, i = conj(ts, i+1)
#         lhs = ast('||', lhs, rhs)
#
#     return lhs, i
#
# def conj(ts: list[token], i: int) -> tuple[ast, int]:
#     """
#     >>> parse('true && false')
#     ast('&&', ast('val', True), ast('val', False))
#     >>> parse('!x && (a && !false)')
#     ast('&&', ast('!', ast('var', 'x')), ast('&&', ast('var', 'a'), ast('!', ast('val', False))))
#     >>> parse('!x && a && !false')
#     ast('&&', ast('&&', ast('!', ast('var', 'x')), ast('var', 'a')), ast('!', ast('val', False)))
#     """
#     if i >= len(ts):
#         raise SyntaxError('expected conjunction, found EOF')
#
#     lhs, i = neg(ts, i)
#
#     while i < len(ts) and ts[i].typ == 'sym' and ts[i].val == '&&':
#         rhs, i = neg(ts, i+1)
#         lhs = ast('&&', lhs, rhs)
#
#     return lhs, i
#
# def neg(ts: list[token], i: int) -> tuple[ast, int]:
#     """
#     >>> parse('! true')
#     ast('!', ast('val', True))
#     >>> parse('!! true')
#     ast('!', ast('!', ast('val', True)))
#     """
#
#     if i >= len(ts):
#         raise SyntaxError('expected negation, found EOF')
#
#     if ts[i].typ == 'sym' and ts[i].val == '!':
#         a, i = neg(ts, i+1)
#         return ast('!', a), i
#     else:
#         return atom(ts, i)
#
# def atom(ts: list[token], i: int) -> tuple[ast, int]:
#     """
#     >>> parse('x')
#     ast('var', 'x')
#     >>> parse('true')
#     ast('val', True)
#     >>> parse('(((false)))')
#     ast('val', False)
#     """
#
#     t = ts[i]
#
#     if t.typ == 'var':
#         return ast('var', t.val), i+1
#     elif t.typ == 'kw' and t.val in ['true', 'false']:
#         return ast('val', t.val == 'true'), i + 1
#     elif t.typ == 'sym' and t.val == '(':
#         a, i = disj(ts, i + 1)
#
#         if i >= len(ts):
#             raise SyntaxError(f'expected right paren, got EOF')
#
#         if not (ts[i].typ == 'sym' and ts[i].val == ')'):
#             raise SyntaxError(f'expected right paren, got "{ts[i]}"')
#
#         return a, i + 1
#
#     raise SyntaxError(f'expected atom, got "{ts[i]}"')

# INTERPRETER

def interp(a: ast, *env: set[str]):
    """
    >>> interp(parse('x || y'), {'y'})
    True
    >>> interp(parse('a || b && c'), {'c'})
    False
    """
    if a.typ == 'val':
        return a.children[0]
    elif a.typ == 'num':
        return float(a.children[0])
    elif a.typ == 'var':
        return a.children[0] in env
    elif a.typ == '!':
        return not interp(a.children[0], env)
    elif a.typ == '&&':
        return interp(a.children[0], env) and interp(a.children[1], env)
    elif a.typ == '||':
        return interp(a.children[0], env) or interp(a.children[1], env)
    elif a.typ == '^':
        return interp(a.children[0]) ** interp(a.children[1])
    elif a.typ == '*':
        return interp(a.children[0]) * interp(a.children[1])
    elif a.typ == '/':
        return interp(a.children[0]) / interp(a.children[1])
    elif a.typ == '%':
        return interp(a.children[0]) % interp(a.children[1])
    elif a.typ == '+':
        return interp(a.children[0]) + interp(a.children[1])
    elif a.typ == '-':
        if len(a.children) == 1:
            return interp(a.children[0])
        return interp(a.children[0]) - interp(a.children[1])

    elif a.typ == '=':
        global RET
        RET[a.children[0].children[0]] = interp(a.children[1])
        return RET

    raise SyntaxError(f'unknown operation {a.typ}')

print(lex('x=2'))
print(parse('x=2'))
print(interp(parse('x=2+1')))
print(RET)
