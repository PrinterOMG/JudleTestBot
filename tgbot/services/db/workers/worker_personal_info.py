from .worker_base import WorkerBase
from .worker_users import WorkerUsers


class WorkerPersonalInfo(WorkerBase):
    _table_name = "presonal_info"
    
    async def create(self) -> None:
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self._table_name} (
            id INT NOT NULL UNIQUE REFERENCES {WorkerUsers._table_name} (id),
            name VARCHAR(255) NOT NULL,
            age SMALLINT NOT NULL,
            city VARHCAR(255) NOT NULL,
            phone VARCHAR(20) NOT NULL
        )
        """
        
        await self.execute(sql)
        
    async def add_personal_info(self, telegram_id: int, name: str, age: int, city: str, phone: str) -> None:
        sql = f"""
        INSERT INTO {self._table_name} (id, name, age, city, phone)
        VALUES (
            (SELECT id FROM {WorkerUsers._table_name} WHERE telegram_id={telegram_id}),
            '{name}',
            {age},
            '{city}',
            '{phone}'
        )
        """
        
        await self.execute(sql)
        
    async def is_user_have_personal_info(self, telegram_id: int) -> bool:
        sql = f"""
        SELECT id FROM {self._table_name}
        WHERE id=(SELECT id FROM {WorkerUsers._table_name} WHERE telegram_id={telegram_id})
        """
        record = await self.fetchone(sql)
        
        return bool(record)
    
    async def get_user_personal_info(self, telegram_id: int) -> dict:
        sql = f"""
        SELECT name, age, city, phone FROM {self._table_name}
        WHERE id=(SELECT id FROM {WorkerUsers._table_name} WHERE telegram_id={telegram_id})
        """
        
        return await self.fetchone(sql)
        