from pymongo import MongoClient

def configure_db(app):
    app.config['MONGO_URI'] = "mongodb://localhost:27017"
    
    client = MongoClient(app.config['MONGO_URI'])
    app.db = client["rule_engine"]
