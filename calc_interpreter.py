#############################
#	Written by Daniel Kats	#
#	December 03 2012		#
#############################

from tree import SyntaxTree
from collections import deque
from multiprocessing import Process, Queue
import operator
import factor # my own factoring module

class InterpreterException(Exception):
	'''General exception caused by interpreter.'''

	pass

def identity(v):
	'''My own unary identity function.'''

	return v

class Interpreter():
	'''An interpreter for arithmetic expressions.
	Recognizes brackets, [+, *, /, -], negative numbers, exponents (^).
	ALWAYS DOES INTEGER DIVISION, DOES NOT RECOGNIZE FLOATS.
	Has persistent variable storage while interpreter is running.

	Standard grammar (a bit informal):
	BinOp = {'+', '-', '*', '/', '^'}
	UnaryOp = {'+', '-'}
	Var = [a-zA-Z]([a-zA-Z0-9] | '.')*
	Number = [+-]?([0-9]+

	Literal = (Var | Number)

	Expr => Literal
	Expr => Expr BinOp Expr
	Expr => UnaryOp Expr
	Expr => '(' Expr ')'

	Syntactic sugar:
	<literal>(<expr>) => <literal> * (<expr>)
	(<expr>)(<expr>) => (<expr>) * (<expr>)

	'''

	binary_ops = set(["+", "-", "*", "/", "^"])
	unary_ops = set(["+", "-", "$"])

	token_priorities = {
		"=" : 0, # higher priorities group closer
		"+" : 1,
		"-" : 1,
		"u$" : 1.5, #let's call this factoring for fun
		"u+" : 2, # unary operator has higher precedent
		"u-" : 2, # unary operator has higher precedent
		"/" : 2,
		"*" : 2,
		"^" : 3,
		"brackets": 4,
	}

	token_ops = {
		"+" : operator.add,
		"-" : operator.sub,
		"u-" : operator.neg,
		"u+" : identity,
		"*" : operator.mul,
		"/" : operator.div,
		"^" : operator.pow,
		"brackets" : identity,
		"u$" :factor.factor
	}


	def __init__(self):
		'''Create a new interpreter.'''

		self._vars = {}

	def token_type(self, token):
		'''Return the type of token that token is.
		This (sort-of) reflects the grammar in the docs.'''

		if token == "(":
			return "open_bracket"
		elif token == ")":
			return "close_bracket"
		elif token in self.binary_ops:
			return "op"
		else:
			return "literal"

	def unsugar(self, token_q):
		'''Replace syntactic sugar with formal spec.''' 

		formal_token_q = deque()
		t2 = token_q.popleft()

		while len(token_q) > 0:
			t1 = t2
			t2 = token_q.popleft()
			formal_token_q.append(t1)

			if (t1 == ")" or self.token_type(t1) == "literal") and t2 == "(":
				formal_token_q.append("*")

		formal_token_q.append(t2)
		return formal_token_q

	def eval(self, expr):
		'''Evalute the expression  return the result.
		Assignment returns None.'''

		token_q = self.tokenize(expr)
		
		# copy over tokens
		token_q_copy = deque(token_q)

		formal_token_q = self.unsugar(token_q)
		try:
			root = self.get_syntax_tree(formal_token_q)
		except InterpreterException as e:
			# some debugging help
			print "ERROR GETTING SYNTAX TREE: %s" % e.message
			print "Tokens:"
			for token in token_q_copy:
				print token
			return
		#root.draw()

		result_q = Queue()
		self.eval_tree(root, result_q)
		return result_q.get()
			
	def eval_tree(self, root, result_q):
		'''Evaluate the syntactic tree specified by root.
		Value is returned in queue passed as argument'''

		if root.is_leaf():
			# literal
			v = root.val
			if v.isdigit():
				result_q.put(int(v)) 
			elif v.count(".") == 1 and v.replace(".", "").isdigit():
				result_q.put(float(v))
			elif v in self._vars:
				result_q.put(self._vars[v])
			else:
				#root.draw()
				raise InterpreterException("Used variable %s before definition" % v)
		elif root.val == "=":
			if root.left.is_leaf():
				var_val = Queue()
				self.eval_tree(root.right, var_val)
				self._vars[root.left.val] = var_val.get()
				result_q.put(None)
			else:
				#root.draw()
				raise InterpreterException("Stop computing things on the left hand side of a variable definition")
		else:
			# regular operation
			if root.right is None:
				root.draw()
				#TODO this doesn't have to be a binary operator
				raise InterpreterException("Binary operator %s requires 2 arguments, got 1" % root.val)
			else:
				right_q = Queue()
				right_process = Process(target = self.eval_tree, args = (root.right, right_q))
				right_process.start()
				#self.eval_tree(root.right, right_q)

			if root.left is None:
				# then operator is unary
				right_process.join() # wait for process to finish
				result_q.put(self.token_ops[root.val](right_q.get()))
			else:
				left_q = Queue()
				left_process = Process(target = self.eval_tree, args = (root.left, left_q))
				left_process.start()
				result_q.put(self.token_ops[root.val](left_q.get(), right_q.get()))

	def get_syntax_tree(self, token_queue):
		'''Return a syntax tree based on the given token queue.
		This method does not resolve syntactic sugar.'''

		active_tree = None

		while len(token_queue) > 0:
			token = token_queue.popleft()

			if token.replace(".", "").isalnum():
				# literals are leaves.
				if active_tree is None:
					active_tree = SyntaxTree(token)
				else:
					active_tree.add_branch(SyntaxTree(token))
			elif token in set(self.token_priorities.keys()) or "u" + token in set(self.token_priorities.keys()):
				if active_tree is None:
					# unary operator, first
					active_tree = SyntaxTree("u" + token, unary=True)
				elif active_tree.is_leaf(): # means active tree is literal
					new_tree = SyntaxTree(token, active_tree.parent) # nest over current active tree
					if not active_tree.is_root():
						active_tree.parent.right = new_tree #re-assign pointer of parent
					new_tree.add_branch(active_tree) # will be left
					
					active_tree = new_tree # move pointer to the new tree
				elif not active_tree.is_full():
					# unary operator, in middle or end
					new_tree = SyntaxTree("u" + token, active_tree, unary=True)
					active_tree.add_branch(new_tree)
					active_tree = new_tree # shift down to unary operator
				else:
					# we use <= to preserve left-right order of operations
					while self.token_priorities[token] <= self.token_priorities[active_tree.val] and not active_tree.is_root():
						active_tree = active_tree.parent

					if self.token_priorities[token] <= self.token_priorities[active_tree.val]:
						new_tree = SyntaxTree(token, active_tree.parent) # nest over active_tree (it's fine if active_tree is root)
						new_tree.add_branch(active_tree)
					else:
						new_tree = SyntaxTree(token, active_tree) # nest under current active tree
						new_tree.add_branch(active_tree.right) # preserve old right branch
						active_tree.right = new_tree # add underneath active tree

					active_tree = new_tree # move pointer to the new tree
			elif token == "(":
				bracket_wrapper = SyntaxTree("brackets", unary=True)
				if active_tree is None:
					active_tree = bracket_wrapper
				else:
					active_tree.add_branch(bracket_wrapper)

				bracket_wrapper.add_branch(self.get_syntax_tree(token_queue))
			elif token == ")":
				return active_tree.get_root()
			
		return active_tree.get_root()

	def tokenize(self, expr):
		'''Take the expression, and extract a Queue of tokens from it. This helps with determining variable names and such.
		Nothing fancy here, just preparing items for the grammar.
		'''

		tokens = deque()
		buffer = ""
		isVar = False
		isFloat = False # not really used

		for c in expr:
			if c.isalpha():
				if not isVar and len(buffer) > 0:
					# we have a number preceding a variable ex. 3c
					tokens.append(buffer)
					buffer = ""
				buffer += c
				isVar = True
			elif c.isdigit():
				# it doesn't matter if var or number 
				buffer += c
			elif c == ".":
				buffer += c
				isVar = False 
				isFloat = True
			else:
				# these are operators of all sorts, brackets, whitespace
				if len(buffer) > 0:
					tokens.append(buffer)
					buffer = ""
					isVar = False

				if len(c.strip()) > 0: # whitespace is not a token
					tokens.append(c)

		# at the end, add any remaining items in buffer to tokens
		if len(buffer) > 0:
			tokens.append(buffer)

		return tokens

