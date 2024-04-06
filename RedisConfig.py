from loguru import logger
import redis
import random
class RedisConfig:
    def __init__(self,config) -> None:
        logger.info("Initiated Redis Config...")
        self.redis_client = redis.StrictRedis(host=config["redis"]["host"], port=config["redis"]["port"], db=0, password=config["redis"]["pass"])
        self.consumer_group = config["redis"]["self.consumer_group"]
        self.stream_key = config["redis"]["self.stream_key"]
    """
    Sending data to Redis (Publisher)
    """
    def pubRedisData(self):
        try:
            # Connect to Redis
            self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, password='redispass')

            # Create a Redis stream
            self.stream_key = 'psmstream'

            # Publish messages to the stream
            for _ in range(1, 11):
                random_number = random.randint(10, 99) 
                message = {'data': f'Message {random_number}'}
                self.redis_client.xadd(self.stream_key, message)

            # Create a consumer group
            self.consumer_group = 'psmgroup'
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
            logger.info(f"group_info - {group_info}")
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
        try:
            # Read messages from the stream
            #redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, password='redispass')
            self.consumer_group = 'psmgroup'
            self.stream_key = 'psmstream'
            while True:
                # Read messages from the stream with a timeout
                messages = self.redis_client.xreadgroup(self.consumer_group, 'psmconsumer', {self.stream_key: '>'}, count=10, block=1000)

                # Process messages
                for stream, data in messages:
                    for message_id, message_data in data:
                        logger.info(f"Received message {message_id}: {message_data}")

                        # Delete the message from the stream
                        self.redis_client.xdel(self.stream_key, message_id)
        except KeyboardInterrupt:
            logger.warning("Program Interrupted !")