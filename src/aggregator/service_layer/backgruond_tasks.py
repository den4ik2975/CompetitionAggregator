import asyncio
from datetime import datetime

from loguru import logger

from src.aggregator.database import crud
from src.aggregator.service_layer.utils import send_email
from src.setup import get_session_maker, setup_email_server


async def send_notifications():
    start = 0
    end = 100
    session_maker = await get_session_maker()
    date_now = datetime.now()

    smtp_server = await setup_email_server()

    logger.info('Sending notifications started')

    while True:
        notifications = await crud.get_limited_notifications(session_maker=session_maker,
                                                             start=start,
                                                             end=end)

        if not notifications:
            break

        for notification in notifications:
            ntf_date = notification.date
            user = await crud.get_user_by_id(session_maker=session_maker,
                                             user_id=notification.user_id)

            if ntf_date.year == date_now.year and ntf_date.month == date_now.month and ntf_date.day == date_now.day + user.n:
                olympiad = await crud.get_olympiad_by_id(session_maker=session_maker,
                                                         olympiad_id=notification.olympiad_id)
                text = f'Напоминание об олимпиаде {olympiad.title}'
                await send_email(email_server=smtp_server,
                                 receiver_email=user.mail,
                                 body=text)
                await crud.delete_notification_by_id(session_maker=session_maker,
                                                     notification_id=notification.id)

            await asyncio.sleep(0)

        start = end
        end += 100

    logger.info('Sending notifications completed')
