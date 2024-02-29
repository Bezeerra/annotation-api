from settings import Settings
import hashlib
from typing import Any


class BaseFuncDB:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.db_session = settings.session_db()

    async def create(self, *args, **kwargs):
        raise NotImplementedError()

    async def update(self, *args, **kwargs):
        raise NotImplementedError()

    async def delete(self, *args, **kwargs):
        raise NotImplementedError()


async def get_hash_by_key(key: Any) -> str:
    key = str(key)
    return hashlib.sha256(key.encode()).hexdigest()
