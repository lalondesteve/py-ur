import asyncio
import logging
from dashboard import get_ursim_ip
from .datatypes import DashboardMessages

logger = logging.getLogger(__name__)
PORT = 29999
_END = b"\r\n"


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
    _value = (" " + value + " ").encode() if value else b""
    try:
        r, w = await asyncio.wait_for(asyncio.open_connection(ip, PORT), 2)
        buf = await r.read(1024)
        if b"Connected" in buf:
            w.write(message.encode() + _value + _END)
            buf = await r.read(1024)
        else:
            raise ConnectionError(buf)
    finally:
        if w:
            w.close()
    return buf.strip()


async def send_batch_messages(ip: str, messages: list[DashboardMessages]):
    w = None
    responses: list[tuple[DashboardMessages, bytes]] = []
    try:
        r, w = await asyncio.wait_for(asyncio.open_connection(ip, PORT), 2)
        buf = await r.read(1024)
        if b"Connected" not in buf:
            raise ConnectionError(buf)
        for m in messages:
            w.write(m.encode() + _END)
            responses.append((m, await r.read(2048)))
    finally:
        if w:
            w.close()
    return responses


if __name__ == "__main__":

    async def run():
        ip = get_ursim_ip()
        print(await check_connection(ip))
        print(await send_message(ip, DashboardMessages.robot_mode))
        # messages = [
        #     DashboardMessages.get_loaded_program,
        #     DashboardMessages.robot_mode,
        #     DashboardMessages.is_program_saved,
        #     DashboardMessages.running,
        #     DashboardMessages.safety_status,
        # ]
        from pprint import pprint

        pprint(
            await send_batch_messages(
                ip,
                [m for m in DashboardMessages if m is not DashboardMessages.shutdown],
            )
        )

    asyncio.run(run())
