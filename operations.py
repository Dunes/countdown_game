import operator


class Operation(object):
	
	def __init__(self, name, op, func):
		self.name = name
		self.op = op
		self.func = func
	
	def __call__(self, x, y):
		return self.func(x, y)
	
	def is_applicable(self, x, y):
		return True


add = Operation("add", "+", operator.add)
subtract = Operation("subtract", "-", operator.sub)
multiply = Operation("multiply", "*", operator.mul)
divide = Operation("divide", "/", 
	func=getattr(operator, "floordiv", None) or operator.div
)
divide.is_applicable = lambda x, y: y != 0 and x % y == 0


operations = (add, subtract, multiply, divide)
