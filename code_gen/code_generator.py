# Code generator clas that converts an AST into low-level IR
class CodeGenerator:
	def __init__(self, ast, optimize=False):
		self.ast = ast
		self.optimize = optimize
		self.code = []
		self.temp_counter = 1  # counter for temporary variables
		self.single_arg_gates = ['not']  # gates that allow one argument
		self.double_arg_gates = ['and', 'or', 'xor']  # gates that allow two arguments

	# Generates a temporary register (auto-increments)
	def _get_temp_reg(self):
		temp_reg = f't{self.temp_counter}'
		self.temp_counter += 1
		return temp_reg

	def _extract_node_content(self, node):
		return str(node.label).split('"')[1]

	# Generic gate expression handler
	def _handle_gate_expression(self, node, parent_identifier):
		children = node.children

		# Extract gate and arguments
		gate_type = self._extract_node_content(children[0])

		# Handle single gate expressions
		if len(children) == 2 and gate_type in self.single_arg_gates:
			return self._handle_single_gate_expression(gate_type, children[1], parent_identifier)

		# Handle double gate expressions
		elif len(children) == 3 and gate_type in self.double_arg_gates:
			if self.optimize:
				return self._handle_optimized_double_gate_expression(gate_type, children[1], children[2], parent_identifier)
			return self._handle_double_gate_expression(gate_type, children[1], children[2], parent_identifier)
		else:
			raise Exception(f"Invalid number of arguments ({len(children)-1}) passed to gate {gate_type.upper()}")

	# Single gate expression handler (e.g. NOT)
	def _handle_single_gate_expression(self, gate_type, arg1_node, parent_identifier):
		# Handle first argument
		if str(arg1_node.label) == 'GateExpression':
			arg1_id = self._handle_gate_expression(arg1_node, parent_identifier)
		else:
			arg1_id = self._extract_node_content(arg1_node)

		temp_reg = self._get_temp_reg()
		self.code.append(f'{gate_type.upper()} {temp_reg}, {arg1_id}')
		return temp_reg  # temporary register to hold result of gate expressions

	# Double gate expression handler (e.g. OR, AND)
	def _handle_double_gate_expression(self, gate_type, arg1_node, arg2_node, parent_identifier):
		# Handle first argument
		if str(arg1_node.label) == 'GateExpression':
			arg1_id = self._handle_gate_expression(arg1_node, parent_identifier)
		else:
			arg1_id = self._extract_node_content(arg1_node)

		# Handle second argument
		if str(arg2_node.label) == 'GateExpression':
			arg2_id = self._handle_gate_expression(arg2_node, parent_identifier)
		else:
			arg2_id = self._extract_node_content(arg2_node)

		temp_reg = self._get_temp_reg()
		self.code.append(f'{gate_type.upper()} {temp_reg}, {arg1_id}, {arg2_id}')
		return temp_reg  # temporary register to hold result of gate expressions

	# Performs logic gate optimization
	# - In an OR gate, if either one of the inputs is 1, then the output is always 1
	# - In an AND gate, if either one of the inputs is 0, then the output is always 0
	def _handle_optimized_double_gate_expression(self, gate_type, arg1_node, arg2_node, parent_identifier):
		arg1_id = None
		arg2_id = None
		if str(arg1_node.label) != 'GateExpression':
			arg1_id = self._extract_node_content(arg1_node)
		if str(arg2_node.label) != 'GateExpression':
			arg2_id = self._extract_node_content(arg2_node)

		# OR gate optimization
		if gate_type == 'or' and (arg1_id == '1' or arg2_id == '1'):
			self.code.append(f'MOV {parent_identifier}, 1')
			return None  # no temporary registers used

		# AND gate optimization
		if gate_type == 'and' and (arg1_id == '0' or arg2_id == '0'):
			self.code.append(f'MOV {parent_identifier}, 0')
			return None  # no temporary registers used

		# No optimization possible
		if arg1_id == None:
			arg1_id = self._get_temp_reg()
			temp_reg = self._handle_gate_expression(arg1_node, arg1_id)
			if temp_reg:
				self.code.append(f'MOV {arg1_id}, {temp_reg}')
		if arg2_id == None:
			arg2_id = self._get_temp_reg()
			temp_reg = self._handle_gate_expression(arg2_node, arg2_id)
			if temp_reg:
				self.code.append(f'MOV {arg2_id}, {temp_reg}')

		# Perform gate operation
		temp_reg = self._get_temp_reg()
		self.code.append(f'{gate_type.upper()} {temp_reg}, {arg1_id}, {arg2_id}')
		return temp_reg


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
			temp_reg = self._handle_gate_expression(val_node, identifier)  # must evaluate gate expression first
			if temp_reg != None:  # required if optimization enabled
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
