from typing import List, Tuple, Any

class token:
    def __init__(self, typ: str, val: str):
        self.type = typ
        self.value = val

    def __repr__(self) -> str:
        return f"token({self.type!r}, {self.value!r})"

def lex(input_string: str) -> List[token]:
    """
    tokenize an input string into a list of tokens.

    >>> lexing('var x = 3')
    [token('var', 'x'), token('sym', '='), token('num', '3')]

    >>> lexing('print x, y')
    [token('kw', 'print'), token('var', 'x'), token('sym', ','), token('var', 'y')]

    >>> lexing('z = 2 + x * y')
    [token('var', 'z'), token('sym', '='), token('num', '2'), token('sym', '+'), token('var', 'x'), token('sym', '*'), token('var', 'y')]

    """
    tokens = []
    i = 0
    while i < len(input_string):
        c = input_string[i]
        if c.isdigit():
            num_str = c
            i += 1
            while i < len(input_string) and input_string[i].isdigit():
                num_str += input_string[i]
                i += 1
            if i < len(input_string) and input_string[i] == '.':
                num_str += '.'
                i += 1
                while i < len(input_string) and input_string[i].isdigit():
                    num_str += input_string[i]
                    i += 1
            tokens.append(token('NUMBER', num_str))
        elif c.isalpha():
            identifier = c
            i += 1
            while i < len(input_string) and (input_string[i].isalnum() or input_string[i] == '_'):
                identifier += input_string[i]
                i += 1
            tokens.append(token('IDENTIFIER', identifier))
        elif c == '+' or c == '-' or c == '*' or c == '/' or c == '%' or c == '^' or c == '=':
            tokens.append(token('OPERATOR', c))
            i += 1
        elif c == '(' or c == ')':
            tokens.append(token('PAREN', c))
            i += 1
        elif c.isspace():
            i += 1
        else:
            raise ValueError(f"Invalid character {c!r} at position {i}")
    return tokens




# PARSING
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

    a, i = disj(ts, 0)

    if i != len(ts):
        raise SyntaxError(f"expected EOF, found {ts[i:]!r}")

    return a

def disj(ts: list[token], i: int) -> tuple[ast, int]:
    """
    >>> parse('true || false')
    ast('||', ast('val', True), ast('val', False))
    """
    if i >= len(ts):
        raise SyntaxError('expected conjunction, found EOF')

    lhs, i = conj(ts, i)

    while i < len(ts) and ts[i].typ == 'sym' and ts[i].val == '||':
        rhs, i = conj(ts, i+1)
        lhs = ast('||', lhs, rhs)

    return lhs, i

def conj(ts: list[token], i: int) -> tuple[ast, int]:
    """
    >>> parse('true && false')
    ast('&&', ast('val', True), ast('val', False))
    >>> parse('!x && (a && !false)')
    ast('&&', ast('!', ast('var', 'x')), ast('&&', ast('var', 'a'), ast('!', ast('val', False))))
    >>> parse('!x && a && !false')
    ast('&&', ast('&&', ast('!', ast('var', 'x')), ast('var', 'a')), ast('!', ast('val', False)))
    """
    if i >= len(ts):
        raise SyntaxError('expected conjunction, found EOF')

    lhs, i = neg(ts, i)

    while i < len(ts) and ts[i].typ == 'sym' and ts[i].val == '&&':
        rhs, i = neg(ts, i+1)
        lhs = ast('&&', lhs, rhs)

    return lhs, i

def neg(ts: list[token], i: int) -> tuple[ast, int]:
    """
    >>> parse('! true')
    ast('!', ast('val', True))
    >>> parse('!! true')
    ast('!', ast('!', ast('val', True)))
    """

    if i >= len(ts):
        raise SyntaxError('expected negation, found EOF')

    if ts[i].typ == 'sym' and ts[i].val == '!':
        a, i = neg(ts, i+1)
        return ast('!', a), i
    else:
        return atom(ts, i)

def atom(ts: list[token], i: int) -> tuple[ast, int]:
    """
    >>> parse('x')
    ast('var', 'x')
    >>> parse('true')
    ast('val', True)
    >>> parse('(((false)))')
    ast('val', False)
    """

    t = ts[i]

    if t.typ == 'var':
        return ast('var', t.val), i+1
    elif t.typ == 'kw' and t.val in ['true', 'false']:
        return ast('val', t.val == 'true'), i + 1
    elif t.typ == 'sym' and t.val == '(':
        a, i = disj(ts, i + 1)

        if i >= len(ts):
            raise SyntaxError(f'expected right paren, got EOF')

        if not (ts[i].typ == 'sym' and ts[i].val == ')'):
            raise SyntaxError(f'expected right paren, got "{ts[i]}"')
        
        return a, i + 1

    raise SyntaxError(f'expected atom, got "{ts[i]}"')

    

a = lex('z2 = (2 + x) * y)')
print(a)
b = parse(a)
print(b)