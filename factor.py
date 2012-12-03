#############################
#	Written by Daniel Kats	#
#	December 03 2012		#
#############################

from math import sqrt, ceil, log
import time
import random

def factor(n, slow=True):
	'''Return a list of factors of n.'''

	# naive way 1 - all factors are < floor(sqrt(n))

	l = []

	if n % 2 == 0:
		if slow:
			l.append(2)
			l.append(n / 2)
		else:
			#yield 2
			#yield n / 2
			pass
	
	i = 1 if n > 2 else 3

	while i <= long(sqrt(n)):
		if n % i == 0:
			if slow:
				l.append(i)
			else:
				#yield i
				pass
			if i != n / i:
				if slow:
					l.append(n / i)
				else:
					#yield n / i
					pass

		i += 2

	return l

def test_factor_evens():
	assert 2 in list(factor(2))
	assert 2 in list(factor(16))
	assert 2 in list(factor(2 ** 26))

def test_factor_primes():
	assert len (list(factor(2))) == 2
	assert len (list(factor(3))) == 2
	assert len (list(factor(5))) == 2
	assert len (list(factor(7))) == 2

def test_factor_composites():
	assert len (list(factor(15))) > 2

def test_factor_perfect_squres():
	assert len (list(factor(9))) == 3
	# must be odd
	assert len (list(factor(27823 ** 2))) % 2 == 1

if __name__ == "__main__":
	#test_factor_evens()
	#test_factor_primes()
	#test_factor_composites()
	#test_factor_perfect_squres()
	#print "All tests passed"

	#t = time.time()

	#print factor(random.randint(5 * 10 ** 12, 5 * 10 ** 13), slow=True)
	for i in range(2):
		print random.randint(5 * 10 ** 12, 5 * 10 ** 13)
	#t = time.time() - t
	#print t
	print factor(10)
