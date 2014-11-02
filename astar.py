from abc import abstractmethod, ABCMeta
from operator import attrgetter
from collections import Iterable

class AStar(object):

	__metaclass__ = ABCMeta

	def children(self, node, start, goal):
		child_states = set()
		for child in self._children(node):
			if child.state not in child_states:
				child.g = node.g + self.move_cost(node, child)
				child.h = self.heuristic(child, start, goal)
				child.parent = node
				yield child
				child_states.add(node.state)
				
	
	@abstractmethod
	def _children(self, node):
		"""Generates children nodes from the given node. Initialising their
		`state'. f, g, and h values are initialised by the caller of _children.
		"""
		raise NotImplementedError()

	@staticmethod
	@abstractmethod
	def heuristic(node, start, goal):
		"""Returns the h value of a node."""
		raise NotImplementedError()

	@staticmethod
	@abstractmethod
	def move_cost(start, finish):
		"""Returns the additional cost of moving from `start' to `finish' -- 
		the g value.
		"""
		raise NotImplementedError()
		
	def search(self, start, goal):
		"""Runs until the solution is found or the state space is exhausted. If the 
		state space is exhausted then the nearest solution is extracted from the
		closed set. This search method typically runs slightly faster than itersearch.
		
		Returns a tuple (solution, closedset).
		If no solution was found then solution is None.
		"""
		closedset = {}
		if isinstance(start, Iterable):
			openset = dict(start)
		else:
			openset = {start.state: start}

		while openset:
			current = min(openset.values(), key=attrgetter("f"))
			if goal in current:
				return self.get_path(current), closedset
			del openset[current.state]
			closedset[current.state] = current
			for node in self.children(current, start, goal):
				if node.state in closedset:
					continue
				old_node = openset.get(node.state)
				if old_node is None or old_node.g > node.g:
					openset[node.state] = node
		return None, closedset

	def itersearch(self, start, goal):
		"""An anytime algorithm that yields better and better results until the 
		target is found or the state space is exhausted.
		"""
		closedset = {}
		if isinstance(start, Iterable):
			openset = dict(start)
		else:
			openset = {start.state: start}

		closest_node = min(openset.values(), key=attrgetter("f"))
		yield self.get_path(closest_node)

		while openset:
			current = min(openset.values(), key=attrgetter("f"))
			if current.f < closest_node.f:
				yield self.get_path(current)
				closest_node = current
			if goal in current:
				return # just yielded current node, no need to yield again
			del openset[current.state]
			closedset[current.state] = current
			for node in self.children(current, start, goal):
				if node.state in closedset:
					continue
				old_node = openset.get(node.state)
				if old_node is None or old_node.g > node.g:
					openset[node.state] = node
		return

	@staticmethod
	def get_path(node):
		"""Recreates the path from the initial state to the given node."""
		path = []
		while node.parent:
			path.append(node)
			node = node.parent
		path.append(node)
		return path[::-1]

class AStarNode(object):

	__metaclass__ = ABCMeta
	
	def __init__(self):
		self.g = 0
		self.h = 0
		self.parent = None
	   
	@property
	def f(self):
		return self.g + self.h
	
	@abstractmethod
	def __contains__(self, goal):
		"""Tests to see if the goal is found in the state that this node 
		represents."""
		raise NotImplementedError()
	
	@property
	@abstractmethod
	def state(self):
		"""The state that the node represents."""
		raise NotImplementedError()
	
	def __eq__(self, other):
		"""Used to check if two nodes represent the same state.
		"""
		return self.state == other.state
	
	def __hash__(self):
		raise NotImplementedError("AStarNodes are not hashable")
		



