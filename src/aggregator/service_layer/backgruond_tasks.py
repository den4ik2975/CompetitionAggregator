import asyncio
from datetime import datetime, timedelta

from loguru import logger

from src.aggregator.database import crud
from src.aggregator.service_layer.utils import send_email, logging_wrapper
from src.setup import get_session_maker, setup_email_server


@logging_wrapper
async def send_notifications():
    start = 0
    end = 100
    session_maker = await get_session_maker()
    now = datetime.now()
    date_now = datetime(now.year, now.month, now.day)

    smtp_server = await setup_email_server()

    logger.info('Sending notifications started')

    async with session_maker() as db_session:
        while True:
            notifications = await crud.get_limited_notifications(session=db_session,
                                                                 start=start,
                                                                 end=end)

            if not notifications:
                break

            for notification in notifications:
                if notification.date == date_now or notification.date == date_now - timedelta(days=1):
                    user = await crud.get_user_by_id(session=db_session,
                                                     user_id=notification.user_id)

                    await send_email(email_server=smtp_server,
                                     receiver_email=user.mail,
                                     body=notification.text)

                    await crud.delete_notification_by_id(session=db_session,
                                                         notification_id=notification.id)

                    await asyncio.sleep(0)

            start = end
            end += 100

    logger.info('Sending notifications completed')
