from .worker_base import WorkerBase


class WorkerUsers(WorkerBase):
    _table_name = "users"
    
    async def create(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self._table_name} (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            balance INT DEFAULT 0
        )
        """
        
        await self.execute(sql)
    
    async def is_user_exists(self, telegram_id: int) -> int | bool:
        sql = f"SELECT id FROM {self._table_name} WHERE telegram_id={telegram_id}"
        
        record = await self.fetchone(sql)
        if record:
            return record["id"]
        return False
    
    async def add_new_user(self, telegram_id: int) -> None:
        sql = f"""
        INSERT INTO {self._table_name} (telegram_id)
        VALUES ({telegram_id})
        """
        
        await self.execute(sql)
        
    async def get_balance(self, telegram_id: int) -> int:
        sql = f"SELECT balance FROM {self._table_name} WHERE telegram_id={telegram_id}"
        
        return (await self.fetchone(sql))["balance"]
    
    async def change_balance(self, telegram_id: int, new_balance: int):
        sql = f"""
        UPDATE {self._table_name}
        SET balance={new_balance}
        WHERE telegram_id={telegram_id}
        """
        
        await self.execute(sql)