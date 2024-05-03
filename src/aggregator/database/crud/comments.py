from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.database import Comment


async def add_comment(user_id: int, olympiad_id: int, text: str, session_maker: async_sessionmaker):
    async with session_maker() as session:
        comment = Comment(
            user_id=user_id,
            olympiad_id=olympiad_id,
            text=text
        )

        session.add(comment)
        await session.commit()
