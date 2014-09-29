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
            print("FAIL")
            print("Input          : {}".format(inv))
            print("Expected output: {}".format(outv))
            print("Actual output  : {}".format(actual_output))
            print("Tree           : {}".format(repr(tree)))


# Labels
do_test('\'hello', '\'hello')
do_test('"hello', 'hello')
do_test('hello', 'hello')
do_test('HELLO', 'HELLO')

# Numbers
do_test('123', '123')
do_test('.6', '.6')
do_test('+8', '+8')
do_test('-3.14', '-3.14')
do_test('1.7e6', '1.7e6')
do_test('-1.7E6', '-1.7E6')

do_test('((1))', '1')
do_test('(1+2', '=1+2')
