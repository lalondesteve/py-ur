import pytest

from dashboard import get_ursim_ip
from dashboard.datatypes import DashboardMessages
from dashboard.dashboard import check_connection, send_message


ip = get_ursim_ip()


@pytest.mark.asyncio
async def test_connection():
    r = await check_connection(ip)
    assert r.split(b":")[0] == b"Connected"


@pytest.mark.asyncio
async def test_communication():
    r = await send_message(ip, DashboardMessages.robot_mode)
    assert r.split(b":")[0] == b"Robotmode"
