from __future__ import print_function

import argparse
import functools
import random
from itertools import combinations

from astar import AStar, AStarNode
from operations import operations
from expressions import Expression, InitialState


class Numbers(object):
	high_cards = [25, 50, 75, 100]
	low_cards = list(range(1,11)) * 2
	max_cards = 6
	target_low = 100
	target_high = 999


class CountdownAStar(AStar):
	
	def __init__(self, ops=operations):
		self.operations = ops
	
	def _children(self, node):
		for operation in self.operations:
			for val1, val2 in combinations(node.numbers, 2):
				expr = None
				if operation.is_applicable(val1, val2):
					expr = Expression(val1, val2, operation)
					yield CountdownNode(expr, self.apply_expr(expr, node.numbers))
				if operation.is_applicable(val2, val1):
					rev_expr = Expression(val2, val1, operation)
					if not expr or rev_expr() != expr():
						yield CountdownNode(rev_expr, self.apply_expr(rev_expr, 
							node.numbers))
	
	@staticmethod
	def apply_expr(expr, values):
		"""Applies an expression to a list of values. Removing the operands to
		the expression and adding the result.
		"""
		values = list(values)
		values.remove(expr.x)
		values.remove(expr.y)
		values.append(expr())
		values.sort()
		return tuple(values)

	@staticmethod
	def heuristic(node, start, goal):
		return min(abs(value - goal) for value in node.numbers)

	@staticmethod
	def move_cost(start, finish):
		return 1 # is zero better?

	def find_from(self, target, values):
		"""Wrapper method for search. Initialises start node and `values' is a 
		tuple and sorted.
		"""
		values = tuple(sorted(values))
		best_value = min(values, key=lambda v: abs(v-target))
		start_node = CountdownNode(InitialState(best_value, values), values)
		return self.search(start_node, target)

	def iter_find_from(self, target, values):
		"""Wrapper method for itersearch. Initialises start node and `values' 
		is a tuple and sorted.
		"""
		values = tuple(sorted(values))
		best_value = min(values, key=lambda v: abs(v-target))
		start_node = CountdownNode(InitialState(best_value, values), values)
		start_node.h = float("inf")
		for eq in self.itersearch(start_node, target):
			yield eq


class CountdownNode(AStarNode):
	
	def __init__(self, expression, numbers):
		super(CountdownNode, self).__init__()
		self.expression = expression
		self.numbers = numbers
	
	def __contains__(self, goal):
		return goal in self.numbers
	
	@property
	def state(self):
		return self.numbers
		
	def __str__(self):
		return str(self.expression)

	def __repr__(self):
		return repr(self.expression)


def argparser():
	p = argparse.ArgumentParser(description="Plays the Countdown numbers game")
	exclusive = p.add_mutually_exclusive_group(required=True)
	exclusive.add_argument("--choose", "-c", nargs=2, type=int, metavar="N",
		help="""Number of cards to choose. First the number of low cards. 
		Second is the number of high cards. Total cards chosen must be equal to
		 {} unless --relaxed is specified. There are a maximum of {} high cards
		 and {} low cards to choose from.
		 """.format(Numbers.max_cards, len(Numbers.high_cards), len(Numbers.low_cards)))
	exclusive.add_argument("--numbers", "-n", nargs="+", type=int, metavar="N",
		help="""Specify cards to use. Number of cards must be {}, unless 
		--relaxed is specified.
		""".format(Numbers.max_cards))
	p.add_argument("--target", "-t", type=int,
		help="""Must be a number between {} and {} unless --relaxed is specified.
		""".format(Numbers.target_low, Numbers.target_high))
	p.add_argument("--relaxed", "-r", default=False, action='store_true',
		help="""Relaxes the problem constraints so the problem doesn't have to 
		exactly match the Countdown numbers game. That is, have exactly {} cards 
		and a target between {} and {}.
		""".format(Numbers.max_cards, Numbers.target_low, Numbers.target_high))
	return p


def error(p, msg):
	p.print_help()
	p.exit(2, "\n" + msg + "\n")

	
def get_parameters():
	
	p = argparser()
	args = p.parse_args()
	if args.choose:
		low_numbers, high_numbers = args.choose
		if not args.relaxed:
			if sum(args.choose) != Numbers.max_cards:
				error(p, "Total number of cards must be 6 when not relaxed.")
		if low_numbers > len(Numbers.low_cards):
			error(p, "Must choose {} low cards or less.".format(len(Numbers.low_cards)))
		if high_numbers > len(Numbers.high_cards):
			error(p, "Must choose {} high cards or less.".format(len(Numbers.high_cards)))
		
		high = random.sample(Numbers.high_cards, high_numbers)
		low = random.sample(Numbers.low_cards, low_numbers)
		numbers = low + high
		
	elif args.numbers:
		if not args.relaxed:
			if len(args.numbers) != Numbers.max_cards:
				error(p, "Total number of cards must be 6 when not relaxed.")
		numbers = args.numbers
	else:
		raise NotImplementedError("Expected either choose args or numbers args to be present.")
	
	if args.target is None:
		target = random.randint(Numbers.target_low, Numbers.target_high)
	else:
		if not args.relaxed and not (Numbers.target_low < args.target <= Numbers.target_high):
			error(p, "Target must be between {} and {} when not relaxed".format(Numbers.target_low, Numbers.target_high))
		target = args.target
	
	return target, tuple(sorted(numbers))
	

def run():
	"""Runs until the solution is found or the state space is exhausted. If the 
	state space is exhausted then the nearest solution is extracted from the
	closed set."""

	target, numbers = get_parameters()

	print("numbers are", list(numbers))
	print("target is", target)	

	equation, closedset = CountdownAStar().find_from(target, numbers)
	
	if equation:
		print(equation_to_str(equation))
	else:
		print("no solution found")
		
		key = functools.partial(CountdownAStar.heuristic, start=None, goal=target)

		del closedset[tuple(sorted(numbers))] # remove start node
		print("size of closed set is", len(closedset))
		closest = min(closedset.values(), key=key)
		print("best in closed set is", closest.expression())
		closest_equation = CountdownAStar.get_path(closest)
		print(equation_to_str(closest_equation))


def iterrun():
	"""An anytime algorithm that yields better and better results until the 
	target is found or the state space is exhausted.
	"""
	target, numbers = get_parameters()

	print("numbers are", list(numbers))
	print("target is", target)	

	for equation in CountdownAStar().iter_find_from(target, numbers):
		print(equation[-1].expression(), equation_to_str(equation))
	
	if target == equation[-1].expression():
		print("Solution found.")
	else:
		print("Solution not found. Best was {}.".format(equation[-1].expression()))

		
def equation_to_str(equation):
	if len(equation) == 1:
		return "[ {} ]".format(equation[0])
	return "[ {} ]".format(", ".join(str(expr) for expr in equation[1:]))

	
if __name__ == "__main__":
	#run()
	iterrun()
