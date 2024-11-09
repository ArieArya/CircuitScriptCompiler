from enum import Enum, auto
from collections import namedtuple

class ASTNode:
	def __init__(self, label):
		self.label = label
		self.children = []  # stores list of child nodes

	def __str__(self):
		return self.label

	def add_child(self, child):
		self.children.append(child)