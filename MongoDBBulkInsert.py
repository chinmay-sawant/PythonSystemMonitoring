from pymongo import MongoClient
from datetime import datetime
import random
from tzlocal import get_localzone
import time
def randomFloat() -> float:
    return round(random.uniform(1, 100), 2)

def getTimeZoneData() -> str:
        # Get the current date and time
        current_time = datetime.now()

        # Get the local timezone
        local_timezone = get_localzone()


      # Convert the current time to the local timezone
        localized_time = current_time.astimezone(local_timezone)

        # Convert the localized time to a string with timezone information
        time_with_timezone_string = localized_time.strftime('%Y-%m-%d %H:%M:%S %Z')
        return time_with_timezone_string

def getDocument() -> str:
    document = {
    "2024-04-07": {
      "hostname": "Chinmay",
      "ipaddress": "192.168.9.1",
      "macaddress": "b8:ae:6b:5a:56:55",
      "timestamp": getTimeZoneData(),
      "health": {
        "cpu": {
          "count": randomFloat(),
          "percent": randomFloat()
        },
        "ram": {
          "total": {
            "$numberLong": "16886128640"
          },
          "used": {
            "$numberLong": "12168069120"
          },
          "percent": randomFloat()
        },
        "disk": [
          {
            "device": "C:\\",
            "mountpoint": "C:\\",
            "total": {
              "$numberLong": "172239089664"
            },
            "used": {
              "$numberLong": "125971353600"
            },
            "free": {
              "$numberLong": "46267736064"
            },
            "percent": randomFloat()
          },
          {
            "device": "D:\\",
            "mountpoint": "D:\\",
            "total": {
              "$numberLong": "850596458496"
            },
            "used": {
              "$numberLong": "327924887552"
            },
            "free": {
              "$numberLong": "522671570944"
            },
            "percent": randomFloat()
          }
        ]
      }
    }
  }
    return document
# Connect to the MongoDB instance running on localhost at port 27017
client = MongoClient('localhost', 27017)

# Alternatively, you can connect using a MongoDB URI
# client = MongoClient('mongodb://localhost:27017/')

# Accessing a database
db = client['psmDB']

# Accessing a collection
collection = db['psmCollection']

# Now you can perform CRUD operations on the collection
# For example, you can insert a document
#post = {"author": "John",
#        "text": "My first MongoDB post!",
#        "tags": ["mongodb", "python", "pymongo"]}
"""
4000 records insertions starts here
"""
# for i in range(4000):
#     
#     print(f"inserting {i}")
#     collection.insert_one(getDocument())
# 
#     if (i + 1) % 1000 == 0:  # Check if i+1 is divisible by 1000
#         time.sleep(1)  # Sl
# You can query the collection
#result = collection.find({})
#result = collection.find().sort("2024-04-07.timestamp", -1)
#finalResults = []
#for document in result:
#    if document["2024-04-07"]["timestamp"] not in finalResults:
#         finalResults.append(document["2024-04-07"]["timestamp"])
#    #print(document["2024-04-07"]["timestamp"])
#print(finalResults)
"""
4000 records insertion ends here
"""
kounter=1
while True:
  print(f"Inserting {kounter} record !")
  collection.insert_one(getDocument())
  time.sleep(1)
  kounter+=1
# Close the connection
client.close()


