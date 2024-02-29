import asyncio
from models import *
from settings import Settings, get_settings
from app.mapping.chat_message import chat


async def create_database(settings: Settings):
    if settings.debug_mode:
        async with settings.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database created")


async def drop_database(settings: Settings):
    if settings.debug_mode:
        try:
            async with settings.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            settings.redis.flushall()
            print("Database dropped")
        except Exception as error:
            print("Nothing to DROP ", error)


async def create_index_chat(settings: Settings):
    if settings.debug_mode:
        # delete all the data from the index
        if await settings.es.indices.exists(index=settings.INDEX_ES_CHAT):
            await settings.es.indices.delete(index=settings.INDEX_ES_CHAT)
            print("Index deleted")
        await settings.es.indices.create(
            index=settings.INDEX_ES_CHAT,
            mappings=chat,
            ignore=400,
        )
        print("Index created")


async def initialize_database(settings: Settings):
    await drop_database(settings)
    await create_database(settings)
    # await create_index_chat(settings)
    await settings.session_db().close()


if __name__ == "__main__":
    settings = get_settings()
    asyncio.run(initialize_database(settings))
