from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://ulsidor:hKnFJ78wFMa2Z3MF@grimoire.shjxx.mongodb.net/?retryWrites=true&w=majority"
LOOT_DATA = "loot_data"
GEMSTONES = "gemstones"
TRINKETS = "trinkets"


class Database:

    def __init__(self) -> None:
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client[LOOT_DATA]
        self.gemstones = self.db[GEMSTONES]
        self.trinkets = self.db[TRINKETS]

    
