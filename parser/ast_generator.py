from lexer.tokenizer import Token
from lexer.enums import TokenClass
from parser.enums import NonTerminals
from parser.tree_node import TreeNode

# Token Classes where we can ignore when building AST
ignore_token_classes = set(
    [TokenClass.SEMICOLON, TokenClass.LPAREN, TokenClass.RPAREN, TokenClass.COMMA]
)


class ASTGenerator:
    def __init__(self, parse_tree):
        self.parse_tree = parse_tree
        self.ast = None

    def build_ast(self, parse_tree_node):
        # Terminal Node - return itself
        if (
            isinstance(parse_tree_node.label, Token)
            and parse_tree_node.label.token_class not in ignore_token_classes
        ):
            return parse_tree_node

        # Program Node - main program node
        elif parse_tree_node.label == NonTerminals.Program.name:
            self.ast = TreeNode(
                NonTerminals.Program.name, self.build_ast(parse_tree_node.children[0])
            )  # only has 1 child
            return self.ast

        # StatementList Node - returns list of statements
        elif parse_tree_node.label == NonTerminals.StatementList.name:
            statements = []
            for node in parse_tree_node.children:
                if node.label == NonTerminals.Statement.name:
                    statements.append(self.build_ast(node))
                elif node.label == NonTerminals.StatementList.name:
                    statements.extend(self.build_ast(node))
            return statements

        # Statement Node
        elif parse_tree_node.label == NonTerminals.Statement.name:
            return self.build_ast(
                parse_tree_node.children[0]
            )  # statement node only has a single child

        # Declaration Node
        elif parse_tree_node.label == NonTerminals.Declaration.name:
            children = []
            for node in parse_tree_node.children:
                next_node = self.build_ast(node)
                if next_node:
                    children.append(next_node)
            return TreeNode(NonTerminals.Declaration.name, children)

        # Assignment Node
        elif parse_tree_node.label == NonTerminals.Assignment.name:
            children = []
            for node in parse_tree_node.children:
                if isinstance(node.label, NonTerminals):
                    children.append(self.build_ast(node))
                else:
                    next_node = self.build_ast(node)
                    if next_node:
                        children.append(next_node)
            return TreeNode(NonTerminals.Assignment.name, children)

        # PrintStmt
        elif parse_tree_node.label == NonTerminals.PrintStmt.name:
            children = []
            for node in parse_tree_node.children:
                next_node = self.build_ast(node)
                if next_node:
                    children.append(next_node)
            return TreeNode(NonTerminals.PrintStmt.name, children)

        # IfStmt
        elif parse_tree_node.label == NonTerminals.IfStmt.name:
            children = []
            for node in parse_tree_node.children:
                if (
                    node.label == NonTerminals.Expression.name
                    or node.label == NonTerminals.Statement.name
                ):
                    children.append(self.build_ast(node))
                else:
                    next_node = self.build_ast(node)
                    if next_node:
                        children.append(next_node)
            return TreeNode(NonTerminals.PrintStmt.name, children)

        # Expression
        elif parse_tree_node.label == NonTerminals.Expression.name:
            return self.build_ast(parse_tree_node.children[0])  # expression has a single child

        # Gate Expression
        elif parse_tree_node.label == NonTerminals.GateExpression.name:
            children = []
            for node in parse_tree_node.children:
                if node.label == NonTerminals.Arguments.name:
                    children.extend(self.build_ast(node))  # extend list of arguments
                else:
                    next_node = self.build_ast(node)  # works for both GateType and Terminals
                    if next_node:
                        children.append(next_node)
            return TreeNode(NonTerminals.GateExpression.name, children)

        # GateType
        elif parse_tree_node.label == NonTerminals.GateType.name:
            return parse_tree_node.children[0]

        # Arguments
        elif parse_tree_node.label == NonTerminals.Arguments.name:
            argument_list = []
            for node in parse_tree_node.children:
                if node.label == NonTerminals.Expression.name:
                    argument_list.append(self.build_ast(node))
                elif node.label == NonTerminals.Arguments_.name:
                    argument_list.extend(self.build_ast(node))  # for Arguments'
            return argument_list

        # Arguments'
        elif parse_tree_node.label == NonTerminals.Arguments_.name:
            argument_list = []
            for node in parse_tree_node.children:
                if node.label == NonTerminals.Arguments.name:
                    argument_list.extend(self.build_ast(node))
            return argument_list

    def __str__(self):
        result = ''

        # Perform DFS to print AST.
        stack = [(self.ast, 0)]
        while stack:
            cur_node, depth = stack.pop()
            result += '  ' * depth + '|-> ' + str(cur_node) + '\n'

            for child_node in cur_node.children[::-1]:  # Reverse so we traverse DFS correctly.
                stack.append((child_node, depth + 1))

        return result
