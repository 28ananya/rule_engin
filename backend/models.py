import re
from collections import Counter
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # "operator" or "operand"
        self.left = left            # Left child node
        self.right = right          # Right child node
        self.value = value          # Operand value (e.g., {"age": "> 30"})

    def to_dict(self):
        """ Convert the Node object to a dictionary for MongoDB storage """
        return {
            "node_type": self.node_type,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "value": self.value
        }

    @staticmethod
    def from_dict(node_dict):
        """ Create a Node object from a dictionary """
        if not node_dict:
            return None
        return Node(
            node_type=node_dict.get("node_type"),
            left=Node.from_dict(node_dict.get("left")),
            right=Node.from_dict(node_dict.get("right")),
            value=node_dict.get("value")
        )


def parse_rule(rule_string):
    # Tokenizing the rule string using regular expressions
    tokens = re.findall(r'\(|\)|AND|OR|[a-zA-Z_]+(?: [><=] \d+| [=] \'[a-zA-Z]+\')', rule_string)

    def _parse_tokens(tokens):
        """Helper function to parse tokens recursively and create AST."""
        stack = []
        operators = []

        def process_operator():
            if len(stack) < 2:
                raise ValueError("Invalid expression: not enough operands for the operator")
            right = stack.pop()
            left = stack.pop()
            operator = operators.pop()
            node = Node(node_type="operator", left=left, right=right, value=operator)
            stack.append(node)

        while tokens:
            token = tokens.pop(0)

            if token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    process_operator()
                if not operators:
                    raise ValueError("Mismatched parentheses: extra closing parenthesis")
                operators.pop()  # Remove '('
            elif token in ['AND', 'OR']:
                while (operators and operators[-1] in ['AND', 'OR']):
                    process_operator()
                operators.append(token)
            else:
                # Operand node (e.g., age > 30 or department = 'Sales')
                key, operator, value = re.split(r' (>|<|=) ', token)
                value = int(value) if value.isdigit() else value.strip("'")
                operand_node = Node(node_type="operand", value={key.strip(): f"{operator} {value}"})
                stack.append(operand_node)
        
        # Process remaining operators
        while operators:
            process_operator()

        if len(stack) != 1:
            raise ValueError("Invalid rule: leftover elements in the stack")

        return stack.pop()

    try:
        ast = _parse_tokens(tokens)
        return ast
    except Exception as e:
        print(f"Error parsing rule: {e}")
        return None


def combine_rules(rule_asts):
    """
    This function takes a list of rule ASTs and combines them into a single AST.
    It uses a most frequent operator heuristic to reduce redundant checks.
    """
    if not rule_asts:
        return None

    # Collect all operators and their frequencies
    operator_counter = Counter()

    def collect_operators(ast):
        if ast.node_type == "operator":
            operator_counter[ast.value] += 1
            collect_operators(ast.left)
            collect_operators(ast.right)

    for ast in rule_asts:
        collect_operators(ast)

    # Sort operators by frequency (most frequent first)
    most_frequent_operator = operator_counter.most_common(1)[0][0] if operator_counter else "AND"

    # Combine ASTs into a single tree using the most frequent operator
    def merge_asts(asts, operator):
        if len(asts) == 1:
            return asts[0]

        # Recursively combine two ASTs at a time
        left = asts[0]
        right = asts[1]
        combined = Node(node_type="operator", left=left, right=right, value=operator)
        return merge_asts([combined] + asts[2:], operator)

    # Combine all rule ASTs using the most frequent operator
    combined_ast = merge_asts(rule_asts, most_frequent_operator)
    return combined_ast

def evaluate_rule(ast, data):
    """
    Recursively evaluate the AST (Abstract Syntax Tree) against the given data.
    
    :param ast: The AST representing the rule.
    :param data: Dictionary with user data, e.g., {"age": 35, "department": "Sales", "salary": 60000}.
    :return: True if the data matches the rule, False otherwise.
    """

    def evaluate_node(node):
        # If it's an operand, check the condition
        if node['node_type'] == 'operand':
            key, condition = list(node['value'].items())[0]  # Get the operand condition
            operator, threshold = condition.split(' ')  # Split the condition into operator and value
            threshold = int(threshold) if threshold.isdigit() else threshold.strip("'")
            
            if operator == '>':
                return data.get(key, 0) > threshold
            elif operator == '<':
                return data.get(key, 0) < threshold
            elif operator == '=':
                return data.get(key) == threshold
        
        # If it's an operator (AND/OR), evaluate recursively on left and right children
        elif node['node_type'] == 'operator':
            left_result = evaluate_node(node['left'])
            right_result = evaluate_node(node['right'])
            
            if node['value'] == 'AND':
                return left_result and right_result
            elif node['value'] == 'OR':
                return left_result or right_result

        return False

    return evaluate_node(ast)
