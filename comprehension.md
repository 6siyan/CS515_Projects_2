
## Siyan @Apr.13.2023
## Description:  
Expressions are formed from:

    constants (like 2 or 3.14159)
    variables (like x, pi)
    the additive binary operators (+ and -)
    the multiplicative operators (* and /)
    binary modulus (%)
    exponentiation (^)
    the unary negation operator (-)
    pre-increment and decrement (like ++x or --z)
    post-increment and decrement (like x++ or z--)
    parentheses

The precedence ordering is, from loosest to tightest:

    + and - operators, left associative
    *, / and % operators, left associative
    ^ operator, right associative
    unary - operator, nonassociative
    ++ and -- operators, nonassociative


Statements are formed from:

    bare expressions
    assignments (x = e, where x must be a variable and e is any expression)
    print statements (print e1, ..., en, where print is followed by one or more comma-separated expressions)


We ignore whitespace: x + 2 is the same as x+2. But be careful: print x is a statement, while printx is a variable name. Newlines cannot occur within an expression.  
只有符号周边的空格才省略。符号和声明分别处理。  

Variable names must start with an alphabetic character; variables can contain alphanumeric characters and underscores.  




## hints:

换行符分隔，忽略空格
