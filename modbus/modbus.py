import asyncio
import logging
import struct
from typing import Sequence
from utils import get_ursim_ip
from .datatypes import Action, RegisterEnum, RegisterValue

logger = logging.getLogger(__name__)
PORT = 502
IP = get_ursim_ip()


def parse_modbus_response(message: bytes) -> RegisterValue:
    addr: int = -1
    value: int = -1
    if len(message) == 9:
        addr, _, _, _, value = struct.unpack("!HHHBH", message)
    elif len(message) == 11:
        addr, _, _, _, _, value = struct.unpack("!HHHBHH", message)
    elif len(message) == 12:
        addr, _, _, _, _, _, value = struct.unpack("!HHHBBHH", message)
    else:
        logger.warning(f"Unexpected message length: {len(message)} {message}")
    return RegisterValue(register=RegisterEnum(addr), value=value)


def build_modbus_message(register: int | tuple, value: int | None = None) -> bytes:
    if isinstance(register, tuple):
        register, value = register
    _id = register  # transaction id - repeated in answer
    _protocol = 0
    _len = 6  # length of message
    _action = Action.WRITE if value else Action.READ  # Function code
    return b"".join(
        x.to_bytes(2, byteorder="big")
        for x in [_id, _protocol, _len, _action, register, value if value else 1]
    )


async def connect(ip: str = IP):
    w = None
    try:
        r, w = await asyncio.wait_for(asyncio.open_connection(ip, PORT), 2)
        # sending random message to check if we're Connected
        w.write(build_modbus_message(register=666))
        await w.drain()
        response = await r.read(1024)
        register = parse_modbus_response(response)
        if register.register.value != 666:
            raise ConnectionError
        yield r, w
    finally:
        if w:
            w.close()
            await w.wait_closed()


async def send_message(message: bytes, ip: str = IP) -> RegisterValue | None:
    response = None
    async for r, w in connect(ip):
        w.write(message)
        await w.drain()
        response = parse_modbus_response(await r.read(1024))
    return response


async def send_batch_messages(
    messages: list[bytes], ip: str = IP
) -> list[RegisterValue]:
    responses: list[RegisterValue] = []
    async for r, w in connect(ip):
        for m in messages:
            w.write(m)
            await w.drain()
            responses.append(parse_modbus_response(await r.read(1024)))
    return responses


async def build_and_send_messages(
    messages: Sequence[RegisterEnum | tuple[RegisterEnum, int]], ip: str = IP
) -> list[RegisterValue]:
    built_messages = []
    for m in messages:
        if isinstance(m, tuple):
            register_value, value = m
            b = build_modbus_message(register=register_value.value, value=value)
        else:
            b = build_modbus_message(m.value)
        built_messages.append(b)
    return await send_batch_messages(ip=ip, messages=built_messages)


if __name__ == "__main__":
    # from utils import get_ursim_ip

    async def run(): ...

    asyncio.run(run())
