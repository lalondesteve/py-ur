import asyncio
import logging
from .datatypes import DashboardMessages

logger = logging.getLogger(__name__)
PORT = 29999
_END = b"\r\n"


async def connect(ip):
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


async def send_message(ip: str, message: DashboardMessages, value: str = ""):
    buf = b""
    _value = (" " + value + " ").encode() if value else b""
    async for r, w in connect(ip):
        w.write(message.encode() + _value + _END)
        await w.drain()
        buf = await r.read(1024)
    return buf.strip()


async def send_batch_messages(ip: str, messages: list[DashboardMessages]):
    responses: list[tuple[DashboardMessages, bytes]] = []

    async for r, w in connect(ip):
        for message in messages:
            w.write(message.encode() + _END)
            await w.drain()
            response = await r.read(1024)
            responses.append((message, response.strip()))
    return responses


if __name__ == "__main__":

    async def run():
        from utils import get_ursim_ip

        ip = get_ursim_ip()
        print(await send_message(ip, DashboardMessages.get_loaded_program))
        messages = [
            DashboardMessages.get_loaded_program,
            DashboardMessages.robot_mode,
            DashboardMessages.is_program_saved,
            DashboardMessages.running,
            DashboardMessages.safety_status,
        ]
        from pprint import pprint

        #
        pprint(
            await send_batch_messages(
                ip,
                [m for m in messages],
            )
        )

    asyncio.run(run())
