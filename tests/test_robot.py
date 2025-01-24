from py_ur import dashboard
from py_ur import modbus
from py_ur.robot import Robot
import pytest


@pytest.fixture
def robot():
    r = Robot()
    return r


async def test_online(robot: Robot):
    await robot.check_online()
    assert robot.online is True


async def test_state(robot: Robot):
    await robot.get_modbus_state()
    await robot.get_dashboard_state()
    assert isinstance(robot.dashboard_state, dict)
    print(robot.dashboard_state)
    for k, v in robot.dashboard_state.items():
        assert isinstance(k, str)
        assert isinstance(v, str | bool)
    for k, v in robot.modbus_state.items():
        assert isinstance(k, modbus.RegisterEnum)
        assert isinstance(v, int)


async def test_send(robot: Robot):
    modbus_value = 167
    modbus_message = (modbus.RegisterEnum.register_128, modbus_value)
    dashboard_message = dashboard.DashboardStatusMessages.is_program_saved
    responses = []

    def cb(data):
        responses.append(data)

    await robot.send(
        modbus_message=modbus_message, dashboard_message=dashboard_message, callback=cb
    )

    dr, mr = responses
    assert mr[0].value == modbus_value
    assert dr[0][1].split(b" ")[0] in (b"true", b"false")
