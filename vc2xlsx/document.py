import logging

import cell_parser
import ometa

logger = logging.getLogger(__name__)

def _letter_to_number(letters):
	n = 0
	for l in letters:
		n *= 26
		n += ord(l.upper()) - 64
	return n

def _xy_to_numbers(x, y):
	x = _letter_to_number(x)
	y = int(y)
	return x, y

class VisiCalcDocument (object):
	current_cell = (1, 1)
	cell_contents = None

	def run_commands(self, command_list):
		for command in command_list:
			command.run_on_doc(self)

	def __init__(self):
		self.contents = {}

	def get_cell(self, x, y):
		tup = _xy_to_numbers(x, y)
		return self.contents.get(tup)

	def set_cell(self, x, y, v):
		tup = _xy_to_numbers(x, y)
		self.contents[tup] = v

	def get_current_value(self):
		return self.contents.get(self.current_cell)

	def set_current_value(self, v):
		self.contents[self.current_cell] = v

	def set_current_cell(self, x, y):
		self.current_cell = _xy_to_numbers(x, y)

	def __repr__(self):
		rv = []
		for (x, y), v in self.contents.iteritems():
			rv.append("{}, {}: {}".format(x, y, v))
		return "VisiCalcDocument({})".format(', '.join(rv))

	def make_excel(self):
		excel_cells = {}
		for k, v in self.contents.iteritems():
			try:
				excel_cells[k] = cell_parser.parse(v).excel()
			except ometa.runtime.ParseError as e:
				logger.error("Couldn't parse cell value {}, using unmodified value.".format(v), exc_info=e)
				excel_cells[k] = v
		return excel_cells

