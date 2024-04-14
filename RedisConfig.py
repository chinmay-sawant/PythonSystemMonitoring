from loguru import logger
import redis
from MongoConfig import MongoConfig
from SystemMonitoring import SystemMonitoring
import json
from datetime import datetime
import time

class RedisConfig:
    def __init__(self,config) -> None:
        self.config = config
        logger.info("Initiated Redis Config...")
        self.redis_client = redis.StrictRedis(host=config["redis"]["host"], port=config["redis"]["port"], db=0, password=config["redis"]["pass"])
        self.consumer_group = config["redis"]["consumer_group"]
        self.stream_key = config["redis"]["stream_key"]
        self.MC = MongoConfig(config)
        self.SM = SystemMonitoring(config)
    """
    Sending data to Redis (Publisher)
    """
    def pubRedisData(self):
        try:
            # Connect to Redis
            #self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, password='redispass')
            # Publish messages to the stream
            #for _ in range(1, 11):
            #    random_number = random.randint(10, 99) 
            #    message = {'data': f'Message {random_number}'}
            message = json.dumps(self.SM.systemData())
            self.redis_client.xadd(self.stream_key, {self.getTodaysDate():message})

            # Create a consumer group
            try:
                self.create_consumer_group_if_not_exists()
            except redis.exceptions.ResponseError:
                logger.error("Consumer Group Exception")
            
            logger.info("Data Inserted !")
        except KeyboardInterrupt:
            logger.warning("Program Interrupted !")

    """
    check if the xgroup exists in redis
    """
    def create_consumer_group_if_not_exists(self):
        # Check if the consumer group already exists
        # redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, password='redispass')
        existing_groups = self.redis_client.xinfo_groups(self.stream_key)
        for group_info in existing_groups:
            #logger.info(f"group_info - {group_info}")
            if group_info['name'] == self.consumer_group.encode():
                logger.info(f"Consumer group '{self.consumer_group}' already exists.")
                return
         # Create the consumer group if it doesn't exist
        self.redis_client.xgroup_create(self.stream_key, self.consumer_group, id='0', mkstream=True)
        logger.info(f"Consumer group '{self.consumer_group}' created.")
    
    """
    Receiving Data from Redis (Subscriber)
    """
    def subRedisData(self):
        subResults = []
        try:
            # Read messages from the stream
            while True:
                # Read messages from the stream with a timeout
                messages = self.redis_client.xreadgroup(self.consumer_group, 'psmconsumer', {self.stream_key: '>'}, count=10, block=1000)

                # Process messages
                for stream, data in messages:
                    for message_id, message_data in data:
                        # Decode the dictionary values
                        decoded_redis_output = {key.decode(): json.loads(value.decode()) for key, value in message_data.items()}

                        logger.info(f"Received message {message_id.decode()}: {decoded_redis_output}")
                        #logger.info(f"Received message {type(message_id.decode())}: {type(decoded_redis_output)}")
                        #MongoJsonObject = {self.config["serverName"]:decoded_redis_output}
                        subResults.append(decoded_redis_output)
                        #print(decoded_redis_output)
                        # Delete the message from the stream
                        self.redis_client.xdel(self.stream_key, message_id)
                if subResults!=[]:
                    [self.MC.InsertOne(x) for x in subResults]
                    subResults=[]
        except KeyboardInterrupt:
            logger.warning("Program Interrupted !")
        
       

    
    def getTodaysDate(self) -> str:   
        # Get today's date
        today_date = datetime.today()

        # Format the date as yyyy-mm-dd
        formatted_date = today_date.strftime('%Y-%m-%d')

        return formatted_date