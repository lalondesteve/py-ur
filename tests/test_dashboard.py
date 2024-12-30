import asyncio
from typing import assert_type
import pytest

from utils import get_ursim_ip
from dashboard.datatypes import DashboardMessages
from dashboard.dashboard import connect, send_message, send_batch_messages


ip = get_ursim_ip()


@pytest.mark.asyncio
async def test_connection():
    async for r, w in connect(ip):
        assert_type(r, asyncio.StreamReader)
        assert w.is_closing() is False
    with pytest.raises(asyncio.TimeoutError):
        async for _ in connect("6.6.6.6"):
            pass
    with pytest.raises(ConnectionRefusedError):
        async for _ in connect("127.0.0.1"):
            pass


@pytest.mark.asyncio
async def test_message():
    r = await send_message(ip, DashboardMessages.robot_mode)
    assert r.split(b":")[0] == b"Robotmode"


@pytest.mark.asyncio
async def test_batch_messages():
    messages = [
        DashboardMessages.robot_mode,
        DashboardMessages.is_program_saved,
        DashboardMessages.running,
    ]
    r = await send_batch_messages(ip, messages)
    assert isinstance(r, list)
    assert isinstance(r[0], tuple)
    assert r[0][1].split(b":")[0] == b"Robotmode"
