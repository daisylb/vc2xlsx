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
        if isinstance(self.operand, BinaryOperations):
            return "{}({})".format(self.operator, self.operand.excel())
        return "{}{}".format(self.operator, self.operand.excel())

class BinaryOperations (object):
    def __init__(self, first, rest):
        self.first = first
        self.rest = rest

    def __repr__(self):
        rest_v = ', '.join('{}, {}'.format(a, b) for a, b in self.rest)
        return "BinaryOperations({}, {})".format(
                repr(self.first),
                rest_v
        )

    def excel(self, suppress_parens=False):
        # VisiCalc used left-to-right evaluation of arithmetic operators, unless
        # overriden by parentheses. For that reason, this class matches a list
        # of non-parenthesised binary operations rather than a single operation,
        # and generates output for all of them.

        operation_count = len(self.rest)

        rv = []
        if operation_count > 1:
            rv.append("(" * (operation_count - 1))

        rv.append(self.first.excel())

        for operator, operand in self.rest[:-1]:
            rv.append(operator)
            rv.append(operand.excel())
            rv.append(")")

        rv.append(self.rest[-1][0])
        rv.append(self.rest[-1][1].excel())
        return "".join(rv)

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
        else:
            return "={}".format(self.value.excel())

class Label (object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Label({})".format(self.value)

    def excel(self):
        return self.value


_grammar = parsley.makeGrammar(r"""
value = binary_ops | sub_value
sub_value =  cell | number | unary_op | parens

binary_ops = sub_value:first binary_rhs+:rest -> BinaryOperations(first, rest)
binary_rhs = ('+' | '-' | '*' | '/'):operator sub_value:operand -> (operator, operand)

unary_op = ('+' | '-'):operator value:operand -> UnaryOperation(operator, operand)

cell = <letter+>:x <digit+>:y -> Cell(x, y)

number = <decimal (('e' | 'E') (digit+))?>:x -> Number(x)
decimal = <(digit+:whole '.'?:dec digit*:point) | ('.':dec digit+:point)>

parens = '(' value:x (')' | end) -> x
""", globals())

def parse(value):
    if value[0] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'\"":
        return Label(value)
    return Value(_grammar(value).value())

if __name__ == "__main__":
    while True:
        i = raw_input("> ")
        result = parse(i)
        print(repr(result))
        print(result.excel())
