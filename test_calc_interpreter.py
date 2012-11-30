#############################
#	Written by Daniel Kats	#
#	November 30 2012		#
#############################

from calc_interpreter import Interpreter

'''
Some test cases for the calculator interpreter.
'''

def test_tokenize(i):
    print i.tokenize("c + 3")
    print i.tokenize("canary + c * 3")
    print i.tokenize("canary + 3c")
    print i.tokenize("canary + c3")
    print i.tokenize("c+canary + 3+c")

def test_get_syntax_tree(i, expr):
    print "#" * (len(expr) + 10)
    print "expr= %s" % expr
    t = i.get_syntax_tree(expr)
    t.draw()

def test_get_syntax_tree_all(i):
    exprs = [
        "3 + 2",
        "3 + 2 + 7",
        "3 + 2 * 7",
        "3 * 2 + 7",
        "3 * (2 + 7)",
        "(3 + 2) * 7",
        "c = 3",
        "c = 5 * (6 + 9)"
    ]

    for expr in exprs:
        test_get_syntax_tree(i, expr)

def test_eval(i, expr):
    print "#" * (len(expr) + 10)
    print "expr= %s" % expr
    print i.eval(expr)

def test_eval_all(i):
    exprs = [
        "3 + 2",
        "3 + 2 + 7",
        "3 + 2 * 7",
        "3 * 2 + 7",
        "3 * (2 + 7)",
        "(3 + 2) * 7",
        "c = 3",
        "5 * (2*c + 9)"
    ]

    for expr in exprs:
        test_eval(i, expr)

def test_unsugar(i, expr):
	print "#" * (len(expr) + 10)
	print "expr = %s" % expr
	token_q = i.tokenize(expr)
	formal_token_q = i.unsugar(token_q)

	print "formal_token_q = Queue(",
	while not formal_token_q.empty():
		print "%s" % formal_token_q.get(),

	print " )"

def test_unsugar_all(i):
	exprs = [
		"3 + 2",
		"3(2)",
		"c(2)",
		"(2 + 3) (1 + 2)"
	]

	for expr in exprs:
		test_unsugar(i, expr)

if __name__ == "__main__":
	i = Interpreter()
	test_unsugar_all(i)
