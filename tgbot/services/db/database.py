import logging

import tgbot.services.db.workers as workers


class Database:    
    @classmethod
    def __init__(cls, host, password, user, database, port):
        cls.host = host
        cls.password = password
        cls.user = user
        cls.database = database
        cls.port = port
        
        cls._connect_data = {
            "host": host,
            "password": password,
            "database": database,
            "user": user,
            "port": port
        }
        
        cls.logger = logging.getLogger(__name__)
        
    @classmethod
    def get_users_worker(cls):
        return workers.WorkerUsers(**cls._connect_data)
    
    async def create_all(self):
        await workers.WorkerUsers(**self._connect_data).create()
        
        self.logger.debug("All tables created")
        
    async def drop_all(self):
        await workers.WorkerUsers(**self._connect_data).drop()
        
        self.logger.debug("All tables droped")
        
        
        