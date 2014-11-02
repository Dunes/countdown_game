

class Expression(object):
	
	def __init__(self, x, y, operation):
		self.x = x
		self.y = y
		self.operation = operation
	
	def __call__(self):
		return self.operation(self.x, self.y)
	
	def evaluate(self):
		return self()
	
	def __str__(self):
		return "{} {} {} = {}".format(
			self.x,
			self.operation.op,
			self.y,
			self.evaluate()
		)
		
	def __repr__(self):
		return "Expression(x={}, y={}, operation={})".format(
			self.x,
			self.y,
			self.operation.name
		)


class InitialState(Expression):

	def __init__(self, best, values):
		self.best = best
		self.values = values
		
	def __call__(self):
		return self.best

	def __str__(self):
		return "INITIAL_STATE"
		
	def __repr__(self):
		return "InitialState(best={}, values={})".format(self.best, self.values)
