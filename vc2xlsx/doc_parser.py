import parsley

class Goto (object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return "Goto({}, {})".format(repr(self.x), repr(self.y))

class Entry (object):
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return "Entry({})".format(repr(self.value))

class Menu (object):
	def __init__(self, command):
		self.command = command

	def __repr__(self):
		return "Menu({})".format(repr(self.command))

_grammar = parsley.makeGrammar(r"""
document = command*:c -> tuple(x for x in c if x)
command = goto_command | menu_command | entry_command | nl
goto_command = '>' <letter+>:x <digit+>:y (':' | nl) -> Goto(x, y)
entry_command = <(letter | digit | '"' | '\'' | '+' | '-' | '(' | '#' | '@') not_nl*>:value -> Entry(value)
menu_command = '/' <(letter | '-') (letter | digit | '$' | '*')*>:command -> Menu(command)
nl = ('\r'? '\n' | '\r') -> None
not_nl = anything:x ?(x not in '\r\n') -> x
""", globals())

def parse(value):
	return _grammar(value.rstrip('\0\r\n\t ')).document()

if __name__ == "__main__":
	import sys

	with open(sys.argv[1]) as f:
		result = parse(f.read())
		print(repr(result))
