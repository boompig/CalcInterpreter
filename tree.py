#############################
#	Written by Daniel Kats	#
#	November 30 2012		#
#############################

class Tree():
	'''Some kind of tree - combination of unary and binary.
	When left branch is specified, then both branches are valid.
	When right branch is specified but not left, then only right branch is valid (unary).
	Pointers are bi-directional.
	'''

	TAB_WIDTH = 2 # has to do with drawing the tree

	def __init__(self, val=None, parent=None, unary=False):
		'''Bunch of default arguments in constructor to make creating tree easier.'''

		self.left = None
		self.right = None
		self.val = val
		self.parent = parent
		self.unary = unary

	def get_root(self):
		'''Return root of this tree.'''

		root = self
		while not root.is_root():
			root = root.parent
		return root

	def is_root(self):
		'''Return whether this tree has no parent trees.'''

		return self.parent is None

	def draw(self, num_tabs=0):
		'''Draw the tree in ASCII. Tree is drawn with root in top-left, and should be viewed from the side.'''

		if num_tabs > 0:
			prefix = "|" + "-" * num_tabs + " "
		else:
			prefix = ""

		print "%s%s" % (prefix, str(self.val))
		if self.left is not None:
			self.left.draw((num_tabs + 1) * self.TAB_WIDTH)
		if self.right is not None:
			self.right.draw((num_tabs + 1) * self.TAB_WIDTH)

	def is_leaf(self):
		'''Return whether this tree is actually the leaf of a tree.
		May be that it is a single-node tree.'''

		return self.left is None and self.right is None

	def is_full(self):
		'''Return True iff all VALID branches of this tree are attached to subtrees.'''

		if self.unary:
			return self.right is not None
		else:
			return self.left is not None and self.right is not None

class SyntaxTree(Tree):
	'''Extension of above to provide some useful functions in parsing the Domain-Specific Language.'''

	def add_branch(self, b):
		'''Add a branch to the syntax tree. Update parent parameters. Branch has to be a tree.'''

		if b.val is None:
			return # do nothing
		b.parent = self
		if self.left is None and not self.unary:
			self.left = b
		else:
			self.right = b

	def add_branch_node(self, val, unary=False):
		'''Add single value node as subtree of current tree. Return the new node. Allow for new node to be unary tree.'''

		new_tree = SyntaxTree(b, self, unary)
		self.add_branch(new_tree)
		return new_tree

def test_draw_tree():
	'''Some tests to make sure drawing trees works.'''

	tree = SyntaxTree("a")
	tree.left = SyntaxTree("b")
	tree.right = SyntaxTree("c")
	tree.draw()

	# separate the tests
	print "=" * 10

	tree = SyntaxTree("a")
	tree.right = SyntaxTree("c")
	tree.draw()

if __name__ == "__main__":
	test_draw_tree()
