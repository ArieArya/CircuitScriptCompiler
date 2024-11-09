from enum import Enum, auto
from collections import namedtuple

class TreeNode:
	def __init__(self, label, children=None):
		self.label = label
		self.children = [] if children == None else children  # stores list of child nodes

	def __str__(self):
		return str(self.label)

	def add_child(self, child):
		self.children.append(child)