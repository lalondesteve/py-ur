import asyncio
import logging
from dashboard import get_ursim_ip
from .datatypes import DashboardMessages

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
    _end = b"\r\n"
    _value = (" " + value + " ").encode() if value else b""
    try:
        r, w = await asyncio.wait_for(asyncio.open_connection(ip, PORT), 2)
        buf = await r.read(1024)
        if b"Connected" in buf:
            w.write(message.encode() + _value + _end)
            buf = await r.read(1024)
        else:
            raise ConnectionError
    finally:
        if w:
            w.close()
    return buf.strip()


if __name__ == "__main__":

    async def run():
        ip = get_ursim_ip()
        print(await check_connection(ip))
        print(await send_message(ip, DashboardMessages.robot_mode))

    asyncio.run(run())
