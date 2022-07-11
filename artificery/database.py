from pymongo import MongoClient

CONNECTION_STRING_ATLAS = "mongodb+srv://ulsidor:hKnFJ78wFMa2Z3MF@grimoire.shjxx.mongodb.net/?retryWrites=true&w=majority"
CONNECTION_STRING_LOCAL = "mongodb://localhost:27017/"
LOOT_DATA = "loot_data"
GEMSTONES = "gemstones"
TRINKETS = "trinkets"


client = MongoClient(CONNECTION_STRING_LOCAL)
db = client[LOOT_DATA]
gemstones = db[GEMSTONES]
trinkets = db[TRINKETS]
        
    
