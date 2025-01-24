import asyncio
from typing import assert_type
import pytest

from py_ur.utils import get_ursim_ip
from py_ur import DashboardStatusMessages
from py_ur.dashboard import connect, send_message, send_batch_messages

ip = get_ursim_ip()


@pytest.mark.asyncio
async def test_connection():
    async with connect(ip) as (r, w):
        assert_type(r, asyncio.StreamReader)
        assert w.is_closing() is False
    with pytest.raises(asyncio.TimeoutError):
        async with connect("6.6.6.6"):
            pass
    with pytest.raises(ConnectionRefusedError):
        async with connect("127.0.0.1"):
            pass


@pytest.mark.asyncio
async def test_message():
    r = await send_message(ip, DashboardStatusMessages.robot_mode)
    assert r.split(b":")[0] == b"Robotmode"


@pytest.mark.asyncio
async def test_batch_messages():
    messages = [
        DashboardStatusMessages.robot_mode,
        DashboardStatusMessages.is_program_saved,
        DashboardStatusMessages.running,
    ]
    r = await send_batch_messages(ip, messages)
    assert isinstance(r, list)
    assert isinstance(r[0], tuple)
    assert r[0][1].split(b":")[0] == b"Robotmode"
