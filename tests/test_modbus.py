# pyright:reportAttributeAccessIssue=none
import random
from typing import assert_type
import pytest
import asyncio

from utils import get_ursim_ip
from modbus.datatypes import StatusRegister, GeneralPurposeRegister
from modbus.modbus import (
    connect,
    build_modbus_message,
    send_message,
    send_batch_messages,
    build_and_send_messages,
)

ip = get_ursim_ip()


@pytest.mark.asyncio
async def test_connection():
    async for r, w in connect(ip):
        assert_type(r, asyncio.StreamReader)
        assert_type(w, asyncio.StreamWriter)
    with pytest.raises(ConnectionRefusedError):
        async for _ in connect("127.0.0.1"):
            pass
    with pytest.raises(asyncio.TimeoutError):
        async for _ in connect("6.6.6.6"):
            pass


@pytest.mark.asyncio
async def test_message():
    message = build_modbus_message(StatusRegister.isPowerOnRobot)
    r = await send_message(ip, message)
    assert r[0] == StatusRegister.isPowerOnRobot
    assert r[-1] in (0, 1)


@pytest.mark.asyncio
async def test_wrtie_message():
    value = random.randint(0, 255)

    message = build_modbus_message(GeneralPurposeRegister.register_128, value)
    r = await send_message(ip, message)
    assert r[0] == GeneralPurposeRegister.register_128
    assert r[-1] == value


@pytest.mark.asyncio
async def test_batch_messages():
    value = random.randint(0, 255)

    messages = [
        StatusRegister.isPowerOnRobot,
        StatusRegister.safetyMode,
        (GeneralPurposeRegister.register_128, value),
    ]
    messages_bytes = [build_modbus_message(m) for m in messages]
    r = await send_batch_messages(ip, messages_bytes)
    assert isinstance(r, list)
    assert isinstance(r[0], list)
    assert r[-1][-1] == value


@pytest.mark.asyncio
async def test_build_and_send():
    value = random.randint(0, 255)
    messages = [
        StatusRegister.isPowerOnRobot,
        StatusRegister.safetyMode,
        (GeneralPurposeRegister.register_128, value),
    ]
    r = await build_and_send_messages(ip, messages)
    assert isinstance(r, list)
    assert isinstance(r[0], list)
    assert r[-1][-1] == value
