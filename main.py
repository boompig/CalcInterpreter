#############################
#	Written by Daniel Kats	#
#	December 03 2012		#
#############################

from cmd import Cmd
from sys import argv, stderr
from calc_interpreter import Interpreter, InterpreterException

#############################
#	Initial Configuration	#
#############################

BANNER_FILE = "banner.txt"

class CalcInterpreterCLI(Cmd):
	'''The commands are:
	vars
	quit / exit
	help
	'''

	def __init__(self, i):

		# Cmd is old-style class, so have to call super like this
		Cmd.__init__(self)

		self._i = i

		self._read_banner()

		self.prompt = "> "
		self.intro = self.banner
		self.default = lambda expr: interpret(i, expr, False)

	def help_help(self):
		'''Show help for help command.'''

		print "Display help for a command"

	def _read_banner(self):
		'''Read the banner from a file and set it to self.banner.'''

		f = open(BANNER_FILE, "r")
		self.banner = f.read()
		f.close()

	def do_quit(self, s):
		'''Alias for exit.'''

		return self.do_exit(s)

	def help_quit(self):
		'''Alias for help exit.'''

		return self.help_exit()

	def do_exit(self, s):
		'''Just exits the command line.'''

		return True

	def help_exit(self):
		print "Exit the interpreter"

	def do_vars(self, s):
		d = self._i._vars
		if len(d) == 0:
			print "No variables declared yet"
		else:
			#print "Variables:"
			for k, v in d.iteritems():
				print "{} ==> {}".format(k, v)

	def help_vars(self):
		print "Display currently declared variables"

def interpret(i, expr, standalone=True):
	'''Main method'''

	try:
		v = i.eval(expr)
		if v is not None:
			print v
	except InterpreterException as ie:
		if standalone:
			print >>stderr, "ERROR %s" % ie.message
			exit(1) # non-zero exit status
		else:
			print "ERROR: %s" % ie.message

if __name__ == "__main__":
	i = Interpreter()

	#TODO cleaner argument parsing
	if "-c" in argv and len(argv) > argv.index("-c") + 1:
		exprs = argv[argv.index("-c") + 1]
		for expr in exprs.split(";"):
			interpret(i, expr)
	else:
		# just a bit of main loop stuff
		cli = CalcInterpreterCLI(i)
		cli.cmdloop()
