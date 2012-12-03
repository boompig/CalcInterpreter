import time
from main import *
from calc_interpreter import Interpreter

if __name__ == "__main__":
	num_iterations = 5
	interpreter = Interpreter()

	n1 = 42115005504928
	n2 = 41863890870357
	exprs = ["$ %d" % n1, "$ %d"% n2, "$ %d + $ %d" % (n1, n2)]

	print "Number of iteartions = %d" % num_iterations

	for i in xrange(num_iterations):
		print "==> Iteration %d" % (i + 1)

		l = [None] * 3

		for idx, expr in enumerate(exprs):
			t = time.time()
			interpreter.eval(expr)
			t = time.time() - t

			print "expr = %s" % expr
			print "time = %f" % t

			l[idx] = t

		print l[0] + l[1] > l[2]
