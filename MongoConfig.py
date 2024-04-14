from pymongo import MongoClient
from datetime import datetime
class MongoConfig:
    def __init__(self,config) -> None:
        self.client = MongoClient(config["mongoDB"]["host"], config["mongoDB"]["port"])
        self.db = self.client['psmDB']
        # Accessing a collection
        self.todayDate = self.getTodaysDate()
        self.collection = self.db[f"{config['serverName']}_{self.getTodaysDate()}"]
        self.config = config
        
    def InsertOne(self,jsonData) -> bool:
        if self.todayDate!=self.getTodaysDate():
            self.collection = self.db[f"{self.config['serverName']}_{self.getTodaysDate()}"]

        result = self.collection.insert_one(jsonData)
        return True if result.inserted_id else False
    
    def closeConnection(self):
        self.client.close()

    def getTodaysDate(self) -> str:   
        # Get today's date
        today_date = datetime.today()

        # Format the date as yyyy-mm-dd
        formatted_date = today_date.strftime('%Y-%m-%d')

        return formatted_date