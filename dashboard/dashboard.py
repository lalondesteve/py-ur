import asyncio
import logging

from dashboard.datatypes import DashboardStatusMessages, DashboardActionMessages

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


async def send_message(
    ip: str, message: DashboardStatusMessages | DashboardActionMessages, value: str = ""
):
    buf = b""
    _value = (" " + value + " ").encode() if value else b""
    async for r, w in connect(ip):
        w.write(message.value.encode() + _value + _END)
        await w.drain()
        buf = await r.read(1024)
    return buf.strip()


async def send_batch_messages(ip: str, messages: list):
    responses: list[
        tuple[DashboardStatusMessages | DashboardActionMessages, bytes]
    ] = []

    async for r, w in connect(ip):
        for message in messages:
            w.write(message.value.encode() + _END)
            await w.drain()
            response = await r.read(1024)
            responses.append((message, response.strip()))
    return responses


if __name__ == "__main__":

    async def run():
        from utils import get_ursim_ip
        from .datatypes import DashboardStatusMessages

        ip = get_ursim_ip()
        print(await send_message(ip, DashboardStatusMessages.get_loaded_program))
        messages = [
            DashboardStatusMessages.get_loaded_program,
            DashboardStatusMessages.robot_mode,
            DashboardStatusMessages.is_program_saved,
            DashboardStatusMessages.running,
            DashboardStatusMessages.safety_status,
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
