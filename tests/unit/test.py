import asyncio

from src.aggregator.service_layer.utils import send_email
from src.setup import setup_email_server


async def test():
    server = await setup_email_server()
    await send_email(server, 'den41k2975@yandex.ru', 'Notification test')
    server.close()


asyncio.run(test())
