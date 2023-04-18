import copy
import sys
from typing import Any

# LEXING

RET = {}
RET_temp = {}
print_flag = 0
class token():
    typ: str
    val: str

    def __init__(self, typ, val):
        self.typ = typ
        self.val = val

    def __repr__(self):
        return f'token({self.typ!r}, {self.val!r})'


def lex(s: str) -> list[token]:

    tokens = []
    i = 0
    is_increment_or_decrement = False

    while i < len(s):
        if s[i].isspace():
            i += 1

        elif s[i].isdigit() or (s[i] == '-' and i + 1 < len(s) and s[i + 1].isdigit()):
            is_negative = False
            if s[i] == '-':
                is_negative = True
                i += 1
            end = i + 1
            while end < len(s) and s[end].isdigit():
                end += 1
            if end < len(s) and s[end] == '.':
                end += 1
                while end < len(s) and s[end].isdigit():
                    end += 1
                if is_negative:
                    tokens.append(token('sym', '-'))
                tokens.append(token('num', s[i:end]))
            else:
                if is_negative:
                    tokens.append(token('sym', '-'))
                tokens.append(token('num', s[i:end]))
            i = end
            is_increment_or_decrement = False

        elif s[i].isalpha():
            end = i + 1
            while end < len(s) and (s[end].isalnum() or s[end] == '_'):
                end += 1
            assert end >= len(s) or not (s[end].isalnum() or s[end] == '_')
            word = s[i:end]
            if end <= len(s) and word in ['true', 'false']:
                tokens.append(token('kw', s[i:end]))
            else:
                tokens.append(token('var', s[i:end]))
            i = end
            is_increment_or_decrement = False
        elif s[i:i + 2] == '==':
            tokens.append(token('sym', '=='))
            i += 2
            is_increment_or_decrement = True
        elif s[i:i + 2] == '>=':
            tokens.append(token('sym', '>='))
            i += 2
            is_increment_or_decrement = True
        elif s[i:i + 2] == '<=':
            tokens.append(token('sym', '<='))
            i += 2
            is_increment_or_decrement = True
        elif s[i:i + 2] == '!=':
            tokens.append(token('sym', '!='))
            i += 2
            is_increment_or_decrement = True
        elif s[i] == '>':
            tokens.append(token('sym', '>'))
            i += 1
            is_increment_or_decrement = False
        elif s[i] == '<':
            tokens.append(token('sym', '<'))
            i += 1
            is_increment_or_decrement = False

        elif s[i] == '=':
            tokens.append(token('sym', '='))
            i += 1
            is_increment_or_decrement = False
        elif s[i:i + 2] == '+=':
            tokens.append(token('sym', '+='))
            i += 2
            is_increment_or_decrement = True
        elif s[i:i + 2] == '-=':
            tokens.append(token('sym', '-='))
            i += 2
            is_increment_or_decrement = True
        elif s[i:i + 2] == '*=':
            tokens.append(token('sym', '*='))
            i += 2
            is_increment_or_decrement = True
        elif s[i:i + 2] == '/=':
            tokens.append(token('sym', '/='))
            i += 2
            is_increment_or_decrement = True
        elif s[i:i + 2] == '%=':
            tokens.append(token('sym', '%='))
            i += 2
            is_increment_or_decrement = True
        elif s[i:i + 2] == '^=':
            tokens.append(token('sym', '^='))
            i += 2
            is_increment_or_decrement = True
        elif s[i] == '!':
            tokens.append(token('sym', '!'))
            i += 1
            is_increment_or_decrement = False
        elif s[i:i + 2] == '++':
            tokens.append(token('sym', '++'))
            i += 2
            is_increment_or_decrement = True
        elif s[i:i + 2] == '--':
            tokens.append(token('sym', '--'))
            i += 2
            is_increment_or_decrement = True
        elif s[i] == '+':
            if i > 0 and (s[i - 1] == '+' or s[i - 1] == '-' or is_increment_or_decrement):
                i += 1
                tokens.append(token('sym', '+'))
            else:
                tokens.append(token('sym', '+'))
                i += 1
            is_increment_or_decrement = False
        elif s[i] == '-':
            if i > 0 and (s[i - 1] == '+' or s[i - 1] == '-' or is_increment_or_decrement):
                i += 1
                tokens.append(token('sym', '-'))
            else:
                tokens.append(token('sym', '-'))
                i += 1
            is_increment_or_decrement = False
        elif s[i] == '*':
            tokens.append(token('sym', '*'))
            i += 1
            is_increment_or_decrement = False
        elif s[i] == '/':
            tokens.append(token('sym', '/'))
            i += 1
            is_increment_or_decrement = False
        elif s[i] == '%':
            tokens.append(token('sym', '/'))
            i += 1
            is_increment_or_decrement = False
        elif s[i] == '^':
            tokens.append(token('sym', '^'))
            i += 1
            is_increment_or_decrement = False
        elif s[i] == '(':
            tokens.append(token('sym', '('))
            i += 1
            is_increment_or_decrement = False
        elif s[i] == ')':
            tokens.append(token('sym', ')'))
            i += 1
            is_increment_or_decrement = False
        elif s[i:i + 2] == '||':
            tokens.append(token('sym', '||'))
            i += 2
            is_increment_or_decrement = False
        elif s[i:i + 2] == '&&':
            tokens.append(token('sym', '&&'))
            i += 2
            is_increment_or_decrement = False
        else:
            raise SyntaxError(f'unexpected character {s[i]}')

    return tokens


# PARSING

class ast():
    typ: str
    children: tuple[Any, ...]

    def __init__(self, typ: str, *children: Any):
        self.typ = typ
        self.children = children

    def __repr__(self):
        return f'ast({self.typ!r}, {", ".join([repr(c) for c in self.children])})'


def parse(s: str) -> ast:
    ts = lex(s)

    # try:
    a, i = assign(ts, 0)
    return a
    # except:
    print('parse error')


def assign(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError('expected assign, found EOF')

    if i + 1 < len(ts) and (ts[i + 1].typ == 'kw' or (ts[i].typ == 'sym' and ts[i].val == '!' or ts[i + 1].val == '&&' or ts[i + 1].val == '||')):
        lhs, i = disj(ts, i)
        while i < len(ts) and ts[i].typ == 'sym' and ts[i].val == '=':
            flag_as = ts[i].val
            rhs, i = disj(ts, i + 1)
            lhs = ast(flag_as, lhs, rhs)
    else:
        lhs, i = add_sub(ts, i)
        while i < len(ts) and ts[i].typ == 'sym' and (ts[i].val == '=' or ts[i].val == '+=' or ts[i].val == '-=' or ts[i].val == '*=' or ts[i].val == '/=' or ts[i].val == '%=' or ts[i].val == '^=' or ts[i].val == '==' or ts[i].val == '>=' or ts[i].val == '<=' or ts[i].val == '!=' or ts[i].val == '>' or ts[i].val == '<'):
            flag_as = ts[i].val
            rhs, i = add_sub(ts, i + 1)
            lhs = ast(flag_as, lhs, rhs)

    return lhs, i


def disj(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError('expected conjunction, found EOF')

    lhs, i = conj(ts, i)

    while i < len(ts) and ts[i].typ == 'sym' and ts[i].val == '||':
        rhs, i = conj(ts, i+1)
        lhs = ast('||', lhs, rhs)

    return lhs, i


def conj(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError('expected conjunction, found EOF')

    lhs, i = neg(ts, i)

    while i < len(ts) and ts[i].typ == 'sym' and ts[i].val == '&&':
        rhs, i = neg(ts, i+1)
        lhs = ast('&&', lhs, rhs)

    return lhs, i


def neg(ts: list[token], i: int) -> tuple[ast, int]:

    if i >= len(ts):
        raise SyntaxError('expected negation, found EOF')

    if ts[i].typ == 'sym' and ts[i].val == '!':
        a, i = neg(ts, i+1)
        return ast('!', a), i
    else:
        return atom(ts, i)
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
    lhs, i = dec_inc(ts, i)

    while i < len(ts) and ts[i].typ == 'sym' and ts[i].val == '^':
        flag_md = ts[i].val
        rhs, i = dec_inc(ts, i + 1)
        lhs = ast(flag_md, lhs, rhs)

    return lhs, i


def dec_inc(ts: list[token], i: int) -> tuple[ast, int]:

    if i >= len(ts):
        raise SyntaxError('expected dec_inc, found EOF')

    if i < len(ts) and (ts[i].typ == 'var' or ts[i].typ == 'num' or ts[i].typ == 'kw' or (ts[i].typ == 'sym' and ts[i].val == ')') or (ts[i].typ == 'sym' and ts[i].val == '(')):
        lhs, i = atom(ts, i)

    if i < len(ts) and ts[i].typ == 'sym' and (ts[i].val == '++' or ts[i].val == '--'):
        if ts[i - 1].typ == 'var':
            flag_dec_inc = 'p' + ts[i].val
        if i + 1 < len(ts) and ts[i + 1].typ == 'var':
            flag_dec_inc = ts[i].val + 'p'
        if i + 1 < len(ts) and (ts[i + 1].typ == 'var' or ts[i + 1].typ == 'num'):
            lhs, i = atom(ts, i + 1)
        return ast(flag_dec_inc, lhs), i + 1

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
        a, i = assign(ts, i + 1)

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

def interp(a: ast):
    global RET
    global RET_temp
    # try:
    if a.typ == 'val':
        return a.children[0]
    elif a.typ == 'num':
        return float(a.children[0])
    elif a.typ == 'var':
        return RET[a.children[0]]

    elif a.typ == '!':
        RET[a.children[0].children[0]] = not RET[a.children[0].children[0]]
        return RET
    elif a.typ == '&&':
        return int(bool(interp(a.children[0])) and bool(interp(a.children[1])))
    elif a.typ == '||':
        return int(bool(interp(a.children[0])) or bool(interp(a.children[1])))

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

    elif a.typ == '>':
        return interp(a.children[0]) > interp(a.children[1])
    elif a.typ == '<':
        return interp(a.children[0]) < interp(a.children[1])
    elif a.typ == '==':
        return interp(a.children[0]) == interp(a.children[1])
    elif a.typ == '>=':
        return interp(a.children[0]) >= interp(a.children[1])
    elif a.typ == '<=':
        return interp(a.children[0]) <= interp(a.children[1])
    elif a.typ == '!=':
        return interp(a.children[0]) != interp(a.children[1])

    elif a.typ == '=':
        RET[a.children[0].children[0]] = interp(a.children[1])
        return RET
    elif a.typ == '+=':
        RET[a.children[0].children[0]] += interp(a.children[1])
        return RET
    elif a.typ == '-=':
        RET[a.children[0].children[0]] -= interp(a.children[1])
        return RET
    elif a.typ == '*=':
        RET[a.children[0].children[0]] *= interp(a.children[1])
        return RET
    elif a.typ == '/=':
        RET[a.children[0].children[0]] /= interp(a.children[1])
        return RET
    elif a.typ == '%=':
        RET[a.children[0].children[0]] %= interp(a.children[1])
        return RET
    elif a.typ == '^=':
        RET[a.children[0].children[0]] **= interp(a.children[1])
        return RET

    elif a.typ == '++p':
        RET[a.children[0].children[0]] = RET[a.children[0].children[0]] + 1
        return RET
    elif a.typ == 'p++':
        RET_temp = copy.deepcopy(RET)
        RET[a.children[0].children[0]] = RET[a.children[0].children[0]] + 1
        return RET_temp[a.children[0].children[0]]
    elif a.typ == '--p':
        RET[a.children[0].children[0]] = RET[a.children[0].children[0]] - 1
        return RET
    elif a.typ == 'p--':
        RET_temp = copy.deepcopy(RET)
        RET[a.children[0].children[0]] = RET[a.children[0].children[0]] - 1
        return RET_temp[a.children[0].children[0]]

    raise SyntaxError(f'unknown operation {a.typ}')
    # except:
    #     pass


def main():
    if len(sys.argv) < 2:
        print('Usage: python script.py filename')
        sys.exit()

    filename = sys.argv[1]

    with open(filename, "r") as file:
        text = file.read()
    start_pos = text.find("/*")
    while start_pos != -1:
        end_pos = text.find("*/", start_pos + 2)
        if end_pos == -1:
            raise ValueError("wrong end")
        text = text[:start_pos] + text[end_pos + 2:]
        start_pos = text.find("/*")
    text_lines = text.split('\n')
    for i, line in enumerate(text_lines):
        comment_pos = line.find('#')
        if comment_pos != -1:
            text_lines[i] = line[:comment_pos]
    text = '\n'.join(text_lines)
    text = '\n'.join([line.strip() for line in text.split('\n') if line.strip()])
    text = text.split('\n')

    global RET

    for line in text:
        if line.startswith('print'):
            print_lines = []
            var_names = [var.strip() for var in line[6:].split(',')]
            for name in var_names:
                temp = interp(parse(name))
                print_lines.append(temp)
            print(' '.join(str(x) for x in print_lines))
        else:
            interp(parse(line.strip()))


if __name__ == '__main__':
    main()


# print(lex('print x'))
# print(parse('print x'))
# print(interp(parse('z  = 2 + x * y')))

