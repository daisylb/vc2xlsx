import parser

def do_test(inv, outv):
    try:
        tree = parser.parse(inv)
        actual_output = tree.excel()
    except Exception as e:
        print("ERROR")
        print(e)
    else:
        if actual_output != outv:
            print(u"FAIL {:>30} \u2192 {:30}".format(inv, actual_output))
            print("    Expected output: {}".format(outv))
            print("    Tree           : {}".format(repr(tree)))
        else:
            print(u"PASS {:>30} \u2192 {:30}".format(inv, outv))


# Labels
do_test('\'hello', '\'hello')
do_test('"hello', '"hello')
do_test('hello', 'hello')
do_test('HELLO', 'HELLO')

# Numbers
do_test('123', '123')
do_test('.6', '.6')
do_test('+8', '+8')
do_test('-3.14', '-3.14')
do_test('1.7e6', '1.7e6')
do_test('-1.7E6', '-1.7E6')

# Binary Operations
do_test('1+1', '=1+1')
do_test('1-2*3', '=(1-2)*3')

# Unary Identity/Negation
do_test('+1', '+1')
do_test('-B6', '=-B6')
do_test('-(2*2)', '=-(2*2)')

# Parentheses
do_test('((1))', '1')
do_test('(1+1)', '=1+1')
do_test('((1', '1')
do_test('(1+2', '=1+2')

# Functions
do_test('@PI', '=PI()')
do_test('@SUM(A1)', '=SUM(A1)')
do_test('@SUM(1,3)', '=SUM(1,3)')
do_test('@SUM(1,3+4,B5)', '=SUM(1,3+4,B5)')
