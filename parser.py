import parsley

class Number (object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Number({})".format(self.value)

    def excel(self):
        return self.value

class Cell (object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Cell({}, {})".format(repr(self.x), repr(self.y))

    def excel(self):
        return "{}{}".format(self.x, self.y)

class UnaryOperation (object):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return "UnaryOperation({}, {})".format(self.operator, self.operand)

    def excel(self):
        return "{}{}".format(self.operator, self.operand.excel())

class Arithmetic (object):
    def __init__(self, operand1, operator, operand2):
        self.operand1 = operand1
        self.operator = operator
        self.operand2 = operand2

    def __repr__(self):
        return "Arithmetic({}, {}, {})".format(
                repr(self.operand1),
                repr(self.operator),
                repr(self.operand2)
        )

    def excel(self, suppress_parens=False):
        # VisiCalc used left-to-right evaluation of arithmetic operators, unless
        # overriden by parentheses.
        # By only allowing explicitly parenthesised arithmetic operators on the
        # RHS, the grammar ensures that the AST's structure matches VisiCalc's
        # order of evaluation.
        # Here, we parenthesise every operation so that Excel will evaluate them
        # the way we want, rather than applying its natural order of operations.
        if suppress_parens:
            fs = "{}{}{}"
        else:
            fs = "({}{}{})"
        return fs.format(
            self.operand1.excel(),
            self.operator,
            self.operand2.excel()
        )

class Value (object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Value({})".format(self.value)

    def excel(self):
        if (isinstance(self.value, Number) or
                (isinstance(self.value, UnaryOperation) and
                    isinstance(self.value.operand, Number))):
            return self.value.excel()
        elif isinstance(self.value, Arithmetic):
            return "={}".format(self.value.excel(suppress_parens=True))
        else:
            return "={}".format(self.value.excel())

class Label (object):
    def __init__(self, first, rest):
        if first == '"':
            self.value = rest
        else:
            self.value = first + rest

    def __repr__(self):
        return "Label({})".format(self.value)

    def excel(self):
        return self.value


_grammar = parsley.makeGrammar(r"""
cell_content = label | value

label = ('"' | '\'' | ' ' | letter):first anything*:rest -> Label(first, ''.join(rest))

value = sub_value:x -> Value(x)
sub_value = arithmetic | rhs_sub_value
rhs_sub_value =  cell | number | parens | unary_operation

arithmetic = sub_value:o1 ('+' | '-' | '*' | '/'):oper rhs_sub_value:o2 -> Arithmetic(o1, oper, o2)

unary_operation = ('+' | '-'):operator sub_value:operand -> UnaryOperation(operator, operand)

cell = '+'? letter:x digit:y -> Cell(x, y)

number = <decimal (('e' | 'E') (digit+))?>:x -> Number(x)
decimal = <(digit+:whole '.'?:dec digit*:point) | ('.':dec digit+:point)>

parens = '(' sub_value:x (')' | end) -> x
""", globals())

def parse(value):
    return _grammar(value).cell_content()

if __name__ == "__main__":
    while True:
        i = raw_input("> ")
        result = parse(i)
        print(repr(result))
        print(result.excel())
