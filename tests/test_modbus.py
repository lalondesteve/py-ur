# pyright:reportAttributeAccessIssue=none
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
    message = modbus.build_modbus_message(modbus.StatusRegister.isPowerOnRobot)
    r = await modbus.send_message(ip, message)
    assert r[0] == modbus.StatusRegister.isPowerOnRobot
    assert r[-1] in (0, 1)


@pytest.mark.asyncio
async def test_wrtie_message():
    value = random.randint(0, 255)

    message = modbus.build_modbus_message(
        modbus.GeneralPurposeRegister.register_128, value
    )
    r = await modbus.send_message(ip, message)
    assert r[0] == modbus.GeneralPurposeRegister.register_128
    assert r[-1] == value


@pytest.mark.asyncio
async def test_batch_messages():
    value = random.randint(0, 255)

    messages = [
        modbus.StatusRegister.isPowerOnRobot,
        modbus.StatusRegister.safetyMode,
        (modbus.GeneralPurposeRegister.register_128, value),
    ]
    messages_bytes = [modbus.build_modbus_message(m) for m in messages]
    r = await modbus.send_batch_messages(ip, messages_bytes)
    assert isinstance(r, list)
    assert isinstance(r[0], list)
    assert r[-1][-1] == value


@pytest.mark.asyncio
async def test_build_and_send():
    value = random.randint(0, 255)
    messages = [
        modbus.StatusRegister.isPowerOnRobot,
        modbus.StatusRegister.safetyMode,
        (modbus.GeneralPurposeRegister.register_128, value),
    ]
    r = await modbus.build_and_send_messages(ip, messages)
    assert isinstance(r, list)
    assert isinstance(r[0], list)
    assert r[-1][-1] == value


@pytest.mark.asyncio
async def test_build_send_and_parse():
    messages = [
        modbus.StatusRegister.isPowerOnRobot,
        modbus.StatusRegister.isEmergencyStopped,
    ]
    responses = [
        modbus.resolve_register(r)
        for r in await modbus.build_and_send_messages(ip, messages)
    ]
    assert responses[0].name == "isPowerOnRobot"
    assert responses[0].value in (0, 1)
    assert responses[1].name == "isEmergencyStopped"
    assert responses[1].value in (0, 1)
