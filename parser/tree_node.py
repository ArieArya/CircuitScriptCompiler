class TreeNode:
	# Represents a node in the parse tree with a label and optional children
    def __init__(self, label, children=None):
        self.label = label
        self.children = [] if children is None else children  # stores list of child nodes

    def __str__(self):
        return str(self.label)

	# Adds a child node to the current node's list of children
    def add_child(self, child):
        self.children.append(child)
