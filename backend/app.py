from flask import Flask
from config import configure_db
from routes import rule_bp
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Create Flask app
app = Flask(__name__)

# Configure MongoDB
configure_db(app)

# Register routes
app.register_blueprint(rule_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
