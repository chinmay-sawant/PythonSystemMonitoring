from loguru import logger
import schedule
import json
from RedisConfig import RedisConfig
logger.add("PythonSystemMonitor.log", rotation="500 MB", level="INFO")
class PSM:

    def __init__(self) -> None:
        logger.info("Initiated Python System Monitoring")
    
    """
    Loading Data from config file 
    """
    def load_config(self,config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    
if __name__ == "__main__":
    try:
        PSM = PSM()
        config = PSM.load_config("config.json")
        RC = RedisConfig(config)
        # serverType can be server/client
        if config["serverType"]=="client":
            schedule.every(2).seconds.do(RC.pubRedisData)
            while True:
                schedule.run_pending()
        elif config["serverType"]=="server":
            schedule.every(2).seconds.do(RC.subRedisData)
            while True:
                schedule.run_pending()
        else:
            logger.error("Check serverType in config.json")
    except KeyboardInterrupt:
            logger.warning("Program Interrupted !")