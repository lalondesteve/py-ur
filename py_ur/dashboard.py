import asyncio
from contextlib import asynccontextmanager
import logging

from .dashboard_datatypes import DashboardStatusMessages, DashboardActionMessages

logger = logging.getLogger(__name__)
PORT = 29999
_END = b"\r\n"


@asynccontextmanager
async def connect(ip: str):
    w = None
    try:
        r, w = await asyncio.wait_for(asyncio.open_connection(ip, PORT), 2)
        buf = await r.read(1024)
        if b"Connected" in buf:
            yield r, w
        else:
            raise ConnectionError(buf.decode())
    finally:
        if w:
            w.close()
            await w.wait_closed()


async def send_message(
    ip: str, message: DashboardStatusMessages | DashboardActionMessages, value: str = ""
):
    buf = b""
    _value = (" " + value + " ").encode() if value else b""
    async with connect(ip) as (r, w):
        w.write(message.value.encode() + _value + _END)
        await w.drain()
        buf = await r.read(1024)
    return buf.strip()


async def send_batch_messages(ip: str, messages: list):
    responses: list[
        tuple[DashboardStatusMessages | DashboardActionMessages, bytes]
    ] = []

    async with connect(ip) as (r, w):
        for message in messages:
            w.write(message.value.encode() + _END)
            await w.drain()
            response = await r.read(1024)
            responses.append((message, response.strip()))
    return responses
