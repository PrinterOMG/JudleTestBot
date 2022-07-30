import logging
import asyncpg


class WorkerBase:
    def __init__(self, database: str, user: str, password: str, host: str, port: int = 5432) -> None:
        self._db_name = database
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        
        self.pool: asyncpg.pool.Pool | None = None
        
        self._logger = logging.getLogger(__name__)
        
    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(database=self._db_name, user=self._user, host=self._host, password=self._password, port=self._port)
        
    async def execute(self, *args, **kwargs) -> None:
        if not self.pool:
            await self.connect()
            
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.execute(*args, **kwargs)
        
    async def fetch(self, *args, **kwargs) -> list[asyncpg.Record]:
        if not self.pool:
            await self.connect()
            
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.fetch(*args, **kwargs)
        
    async def fetchone(self, *args, **kwargs) -> asyncpg.Record:
        if not self.pool:
            await self.connect()
            
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.fetchrow(*args, **kwargs)
            
    async def drop(self):
        sql = f"DROP TABLE {self._table_name}"
        
        await self.execute(sql)

