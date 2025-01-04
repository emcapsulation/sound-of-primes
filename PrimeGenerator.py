import sympy as sp

class PrimeGenerator:
	def __init__(self):
		pass


	# Get the list of prime factors of n (with multiplicity)
	def get_prime_factors(self, n):
		# A dictionary of prime factors and their counts
		factors = sp.factorint(n)  

		# A list of prime factors, repeated according to their counts
		return [prime for prime, count in factors.items() for _ in range(count)]


	# Get the total number of prime factors of n (with multiplicity)
	def get_num_prime_factors(self, n):
		return len(self.get_prime_factors(n))