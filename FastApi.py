from fastapi import FastAPI
from starlette.responses import StreamingResponse , FileResponse
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import json
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# Mount the static files directory
#app.mount("/psm", StaticFiles(directory="./dist"), name="static")
def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def getTodaysDate() -> str:   
    # Get today's date
    today_date = datetime.today()
    # Format the date as yyyy-mm-dd
    formatted_date = today_date.strftime('%Y-%m-%d')
    return formatted_date

jsonConfig =  load_config("config.json")


# Connect to the MongoDB instance running on localhost at port 27017
client = AsyncIOMotorClient('localhost', 27017)

# Alternatively, you can connect using a MongoDB URI
# client = MongoClient('mongodb://localhost:27017/')

# Accessing a database
db = client['psmDB']

# Accessing a collection
collection = db[f"{jsonConfig['serverName']}_{getTodaysDate()}"]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin (not recommended for production)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

async def data_stream():
    # Simulate streaming data (in this case, just numbers from 1 to 10)
    for i in range(1, 11):
        yield f"data: {i}\n\n"
        await asyncio.sleep(1)  # Simulate delay between data points


async def getRecordFromMongoDb():
    # Assuming 'collection' is your MongoDB collection instance
    result = await collection.find_one({}, sort=[(f"{getTodaysDate()}.timestamp", -1)])
    asyncio.timeout(1)
    return result

@app.get("/stream")
async def stream_data():
    async def generate():
        while True:
            record = await getRecordFromMongoDb()
            if record:
                # Convert ObjectId to string before serializing to JSON
                record["_id"] = str(record["_id"])
                json_chunk = json.dumps(record)
                yield f"data: {json_chunk}\n\n"
                  # Introduce a delay of 1 second
                await asyncio.sleep(1)

    # Yield the serialized JSON chunk
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/home")
async def get_html_file():
    return FileResponse("./webfolder/home.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)