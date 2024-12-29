import asyncio
import logging
from enum import IntEnum

logger = logging.getLogger(__name__)
PORT = 502


class Action(IntEnum):
    READ = 3
    WRITE = 6


class StatusRegister(IntEnum):
    robotMode = 258
    isPowerOnRobot = 260
    isSecurityStopped = 261
    isEmergencyStopped = 262
    isTeachButtonPressed = 263
    isPowerButtonPressed = 264
    isSafetySignalSuchThatWeShouldStop = 265
    safetyMode = 266


def parse_modbus_response(message: bytes):
    data = [message[i : i + 2] for i in range(0, len(message), 2)]
    int_data = [int.from_bytes(i) for i in data]
    return int_data


def build_modbus_message(register: int, value: int = 1, action: Action = Action.WRITE):
    _id = register
    _protocol = 0
    _len = 6
    _action = action
    return b"".join(
        x.to_bytes(2, byteorder="big")
        for x in [_id, _protocol, _len, _action, register, value]
    )


async def connect(ip: str):
    try:
        r, w = await asyncio.wait_for(asyncio.open_connection(ip, PORT), 2)
        # sending random message to check if we're Connected
        w.write(build_modbus_message(register=666, action=Action.READ))
        await w.drain()
        response = await r.read(1024)
        data = parse_modbus_response(response)
        if data[0] != 666:
            raise ConnectionError
    except asyncio.TimeoutError:
        await asyncio.sleep(1)
        return connect(ip)
    except Exception as e:
        raise e
    else:
        return r, w


if __name__ == "__main__":
    from dashboard import get_ursim_ip

    async def run():
        ip = get_ursim_ip()
        await connect(ip)

    asyncio.run(run())
