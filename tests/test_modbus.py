import random
from typing import assert_type
import pytest
import asyncio

from utils import get_ursim_ip
import modbus

ip = get_ursim_ip()


@pytest.mark.asyncio
async def test_connection():
    async for r, w in modbus.connect(ip):
        assert_type(r, asyncio.StreamReader)
        assert_type(w, asyncio.StreamWriter)
    with pytest.raises(ConnectionRefusedError):
        async for _ in modbus.connect("127.0.0.1"):
            pass
    with pytest.raises(asyncio.TimeoutError):
        async for _ in modbus.connect("6.6.6.6"):
            pass


@pytest.mark.asyncio
async def test_message():
    message = modbus.build_modbus_message(modbus.RegisterEnum.isPowerOnRobot)
    r = await modbus.send_message(ip, message)
    assert r is not None
    assert r.register == modbus.RegisterEnum.isPowerOnRobot
    assert r.value in (0, 1)


@pytest.mark.asyncio
async def test_write_message():
    value = random.randint(0, 255)

    message = modbus.build_modbus_message(
        modbus.RegisterEnum.register_128, value
    )
    r = await modbus.send_message(ip, message)
    assert r is not None
    assert r.register == modbus.RegisterEnum.register_128
    assert r.value == value


@pytest.mark.asyncio
async def test_batch_messages():
    value = random.randint(0, 65535)

    messages = [
        modbus.RegisterEnum.isPowerOnRobot,
        modbus.RegisterEnum.safetyMode,
        (modbus.RegisterEnum.register_128, value),
    ]
    messages_bytes = [modbus.build_modbus_message(m) for m in messages]
    r = await modbus.send_batch_messages(ip, messages_bytes)
    assert isinstance(r, list)
    assert isinstance(r[0], modbus.RegisterValue)
    assert r[-1].value == value


@pytest.mark.asyncio
async def test_build_and_send():
    value = random.randint(0, 65535)
    messages = [
        modbus.RegisterEnum.isPowerOnRobot,
        modbus.RegisterEnum.safetyMode,
        (modbus.RegisterEnum.register_128, value),
    ]
    r = await modbus.build_and_send_messages(ip, messages)
    assert isinstance(r, list)
    assert isinstance(r[0], modbus.RegisterValue)
    assert r[-1].value == value


@pytest.mark.asyncio
async def test_build_send_and_parse():
    messages = [
        modbus.RegisterEnum.isPowerOnRobot,
        modbus.RegisterEnum.isEmergencyStopped,
    ]
    responses = await modbus.build_and_send_messages(ip, messages)
    print("Responses", responses)
    assert responses[0].register == modbus.RegisterEnum.isPowerOnRobot
    assert responses[0].value in (0, 1)
    assert responses[1].register == modbus.RegisterEnum.isEmergencyStopped
    assert responses[1].value in (0, 1)
