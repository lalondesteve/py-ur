import asyncio
import logging

from .datatypes import Action, Register

logger = logging.getLogger(__name__)
PORT = 502


def parse_modbus_response(message: bytes) -> list[int]:
    data = [message[i : i + 2] for i in range(0, len(message), 2)]
    int_data = [int.from_bytes(i) for i in data]
    return int_data


def build_modbus_message(register: int | tuple, value: int | None = None) -> bytes:
    if isinstance(register, tuple):
        register, value = register
    _id = register
    _protocol = 0
    _len = 6
    _action = Action.WRITE if value else Action.READ
    return b"".join(
        x.to_bytes(2, byteorder="big")
        for x in [_id, _protocol, _len, _action, register, value if value else 1]
    )


async def connect(ip: str):
    w = None
    try:
        r, w = await asyncio.wait_for(asyncio.open_connection(ip, PORT), 2)
        # sending random message to check if we're Connected
        w.write(build_modbus_message(register=666))
        await w.drain()
        response = await r.read(1024)
        data = parse_modbus_response(response)
        if data[0] != 666:
            raise ConnectionError
        yield r, w
    finally:
        if w:
            w.close()
            await w.wait_closed()


async def send_message(ip: str, message: bytes) -> list[int]:
    response: list[int] = []
    async for r, w in connect(ip):
        w.write(message)
        await w.drain()
        response = parse_modbus_response(await r.read(1024))
    return response


async def send_batch_messages(ip: str, messages: list[bytes]) -> list[list[int]]:
    responses: list[list[int]] = []
    async for r, w in connect(ip):
        for m in messages:
            w.write(m)
            await w.drain()
            responses.append(parse_modbus_response(await r.read(1024)))
    return responses


async def build_and_send_messages(
    ip: str, messages: list[Register | tuple[Register, int]]
) -> list[list[int]]:
    built_messages = []
    for m in messages:
        if isinstance(m, tuple):
            register, value = m
            b = build_modbus_message(register=register.value, value=value)
        else:
            b = build_modbus_message(m.value)
        built_messages.append(b)
    return await send_batch_messages(ip, built_messages)


if __name__ == "__main__":
    # from utils import get_ursim_ip

    async def run():
        ...
        # ip = get_ursim_ip()
        # messages = [
        #     StatusRegister.isPowerOnRobot,
        #     (GeneralPurposeRegister.register_128, 124),
        # ]
        # responses = await build_and_send_messages(ip, messages)
        # print(responses)

    asyncio.run(run())
