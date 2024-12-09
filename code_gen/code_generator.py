# Code generator clas that converts an AST into low-level IR
class CodeGenerator:
	def __init__(self, ast):
		self.ast = ast
		self.code = []
		self.temp_counter = 1  # counter for temporary variables
		self.single_arg_gates = ['not']  # gates that allow one argument
		self.double_arg_gates = ['and', 'or', 'xor']  # gates that allow two arguments

	def _extract_node_content(self, node):
		return str(node.label).split('"')[1]

	def _handle_single_gate_expression(self, gate_type, arg1_node):
		# Handle first argument
		if str(arg1_node.label) == 'GateExpression':
			arg1_id = self._handle_gate_expression(arg1_node)
		else:
			arg1_id = self._extract_node_content(arg1_node)

		temp_reg = f't{self.temp_counter}'
		self.code.append(f'{gate_type.upper()} {temp_reg}, {arg1_id}')
		self.temp_counter += 1
		return temp_reg  # temporary register to hold result of gate expressions

	def _handle_double_gate_expression(self, gate_type, arg1_node, arg2_node):
		# Handle first argument
		if str(arg1_node.label) == 'GateExpression':
			arg1_id = self._handle_gate_expression(arg1_node)
		else:
			arg1_id = self._extract_node_content(arg1_node)

		# Handle second argument
		if str(arg2_node.label) == 'GateExpression':
			arg2_id = self._handle_gate_expression(arg2_node)
		else:
			arg2_id = self._extract_node_content(arg2_node)

		temp_reg = f't{self.temp_counter}'
		self.code.append(f'{gate_type.upper()} {temp_reg}, {arg1_id}, {arg2_id}')
		self.temp_counter += 1
		return temp_reg  # temporary register to hold result of gate expressions

	def _handle_gate_expression(self, node):
		children = node.children

		# Extract gate and arguments
		gate_type = self._extract_node_content(children[0])

		# Handle single gate expressions
		if len(children) == 2 and gate_type in self.single_arg_gates:
			return self._handle_single_gate_expression(gate_type, children[1])
		# Handle double gate expressions
		elif len(children) == 3 and gate_type in self.double_arg_gates:
			return self._handle_double_gate_expression(gate_type, children[1], children[2])
		else:
			raise Exception(f"Invalid number of arguments ({len(children)-1}) passed to gate {gate_type.upper()}")

	def _handle_declaration(self, node):
		children = node.children

		# Extract identifier and value node
		identifier_type = self._extract_node_content(children[0])
		identifier = self._extract_node_content(children[1])
		val_node = children[3]

		# 1. Register declaration
		if identifier_type == 'reg' and 'DIGIT' in str(val_node.label):
			val = self._extract_node_content(val_node)
			self.code.append(f'LOAD {identifier}, {val}')

		# 2. Wire declaration
		elif identifier_type == 'wire' and str(val_node.label) == 'GateExpression':
			temp_reg = self._handle_gate_expression(val_node)  # must evaluate gate expression first
			self.code.append(f'MOV {identifier}, {temp_reg}')

		# Handle invalid declarations
		else:
			raise Exception(f'Invalid declaration of {identifier_type} {identifier}')

	def _handle_print_statement(self, node):
		children = node.children

		# Extract identifier to print
		identifier = self._extract_node_content(children[1])
		self.code.append(f'PRINT {identifier}')

	def generate_ir(self):
		# Iterate over AST
		for node in self.ast.children:
			if node.label == 'Declaration':
				self._handle_declaration(node)
			if node.label == 'PrintStmt':
				self._handle_print_statement(node)

	def get_code_str(self):
		return '\n'.join(self.code)
