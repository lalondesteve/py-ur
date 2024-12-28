import asyncio
import logging
from dashboard import DashboardMessages

logger = logging.getLogger(__name__)
PORT = 29999


async def check_connection(ip):
    w = None
    try:
        r, w = await asyncio.wait_for(asyncio.open_connection(ip, PORT), 2)
        buf = await r.read(1024)
    finally:
        if w:
            w.close()
    return buf.strip()


async def send_message(ip: str, message: DashboardMessages, value: str = ""):
    w = None
    try:
        r, w = await asyncio.wait_for(asyncio.open_connection(ip, PORT), 2)
        buf = await r.read(1024)
        if b"Connected" in buf:
            w.write(message.encode() + b" " + value.encode() + b"\r\n")
            buf = await r.read(1024)
        else:
            raise ConnectionError
    finally:
        if w:
            w.close()
    return buf.strip()


if __name__ == "__main__":

    async def run():
        ip = "lals-t1.netbird.cloud"
        print(await check_connection(ip))
        print(await send_message(ip, DashboardMessages.robot_mode))

    asyncio.run(run())
