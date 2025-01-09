from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from .models import RobotConfigModel


async def add_db_engine(app):
    engine = create_async_engine("sqlite+aiosqlite:///./pyur.db")

    async with engine.begin() as conn:
        await conn.run_sync(RobotConfigModel.metadata.create_all)

    app.ctx.DB = engine


async def get_async_session(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def drop_db(app):
    async with app.ctx.DB.begin() as conn:
        await conn.run_sync(RobotConfigModel.metadata.drop_all)
    await add_db_engine(app)
