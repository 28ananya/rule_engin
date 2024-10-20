from flask import Blueprint, request, jsonify, current_app,render_template
from models import Node, parse_rule, combine_rules
from models import  evaluate_rule 
rule_bp = Blueprint('rule_bp', __name__)

@rule_bp.route('/')
def index():
    return render_template('index.html')

# Create a rule and store it in MongoDB
@rule_bp.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json.get("rule_string")
    rule_name = request.json.get("rule_name")
    
    # Parse rule string to AST
    ast = parse_rule(rule_string)
    
    if ast is None:
        return jsonify({"error": "Invalid rule string"}), 400
    
    # Store AST in MongoDB
    current_app.db.rules.insert_one({
        "rule_name": rule_name,
        "ast": ast.to_dict()
    })
    
    return jsonify({"message": "Rule created", "ast": ast.to_dict()}), 201

# Combine multiple rules into a single AST
@rule_bp.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    rules = request.json.get("rules")  # List of rule names
    
    # Fetch ASTs from MongoDB
    asts = []
    for rule_name in rules:
        rule = current_app.db.rules.find_one({"rule_name": rule_name})
        if rule:
            asts.append(Node.from_dict(rule["ast"]))
    
    if len(asts) < 2:
        return jsonify({"error": "Not enough rules to combine"}), 400
    
    # Call the combine_rules function to combine the rules
    combined_ast = combine_rules(asts)
    
    if combined_ast is None:
        return jsonify({"error": "Failed to combine rules"}), 500

    return jsonify({"combined_ast": combined_ast.to_dict()}), 200

# Evaluate rule against user data
@rule_bp.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_route():
    rule_name = request.json.get("rule_name")
    user_data = request.json.get("data")
    
    # Fetch AST from MongoDB based on the rule name
    rule = current_app.db.rules.find_one({"rule_name": rule_name})
    
    if not rule:
        return jsonify({"error": "Rule not found"}), 404
    
    # Convert the stored AST back into a Node structure
    ast = Node.from_dict(rule["ast"])

    # Call the evaluate_rule function to check if the user data matches the rule
    result = evaluate_rule(ast.to_dict(), user_data)  # Assuming evaluate_rule works with dictionary AST

    return jsonify({"eligible": result}), 200