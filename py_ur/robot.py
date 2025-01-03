import asyncio
from typing import Callable

from . import dashboard
from .dashboard import DashboardActionMessages, DashboardStatusMessages
from . import modbus
import logging
import json

from .utils import get_ursim_ip

logger = logging.getLogger(__name__)


class Robot:
    def __init__(
        self, ip: str = get_ursim_ip(), message_callback: Callable | None = None
    ):
        self.ip = ip
        self.message_callback = message_callback
        self.online = False
        self.modbus_online = False
        self.dashboard_online = False
        self.modbus_status = dict()
        self.dashboard_status = dict()
        self.user_registers = dict()

    async def check_online(self):
        mw = dw = None
        try:
            async for _, mw in modbus.connect(self.ip):
                if mw is None:
                    self.modbus_online = False
                else:
                    self.modbus_online = True
            async for _, dw in dashboard.connect(self.ip):
                if dw is None:
                    self.dashboard_online = False
                else:
                    self.dashboard_online = True
        except Exception as e:
            self.online = False
            logger.debug(e)
        else:
            self.online = any([self.modbus_online, self.dashboard_online])
            logger.debug(f"online: {self.online}")

    async def get_modbus_status(self):
        responses = await modbus.build_and_send_messages(
            ip=self.ip,
            messages=[
                m for m in modbus.RegisterEnum if not m.name.startswith("register_")
            ],
        )
        self.modbus_status = {
            response.register: response.value for response in responses
        }

    async def get_register_status(self, registers: list[modbus.RegisterEnum]):
        print(await modbus.build_and_send_messages(ip=self.ip, messages=registers))

    async def get_dashboard_status(self):
        responses = [
            await dashboard.send_batch_messages(ip=self.ip, messages=[m])
            for m in DashboardStatusMessages
        ]
        self.dashboard_status = {
            response[0][0].name: self.filter_dashboard_responses(
                response[0][1].decode()
            )
            for response in responses
        }

    async def send(
        self,
        modbus_message: list[modbus.RegisterEnum | tuple[modbus.RegisterEnum, int]]
        | modbus.RegisterEnum
        | tuple[modbus.RegisterEnum, int]
        | None = None,
        dashboard_message: list[DashboardActionMessages | DashboardStatusMessages]
        | DashboardActionMessages
        | DashboardStatusMessages
        | None = None,
        callback: Callable | None = None,
    ):
        if not callback:
            callback = self.message_callback
        if dashboard_message:
            if not isinstance(dashboard_message, list):
                dashboard_message = [dashboard_message]
            response = await dashboard.send_batch_messages(
                ip=self.ip, messages=dashboard_message
            )
            if callback and response:
                callback(response)

        if modbus_message:
            if not isinstance(modbus_message, list):
                modbus_message = [modbus_message]
            response = await modbus.build_and_send_messages(
                ip=self.ip, messages=modbus_message
            )
            if callback and response:
                callback(response)

    @staticmethod
    def filter_dashboard_responses(response: str):
        if ":" in response:
            response = response.split(":")[1].strip()
        if len(words := response.split(" ")) > 1:
            response = words[0]
        try:
            response = json.loads(response)
        except json.JSONDecodeError:
            pass
        return response

    async def power_on(self):
        await self.send(dashboard_message=DashboardActionMessages.power_on)

    async def power_off(self):
        await self.send(dashboard_message=DashboardActionMessages.power_off)

    async def brake_release(self):
        await self.send(dashboard_message=DashboardActionMessages.brake_release)

    async def play(self):
        await self.send(dashboard_message=dashboard.DashboardActionMessages.play)

    async def stop(self):
        await self.send(dashboard_message=dashboard.DashboardActionMessages.stop)

    async def pause(self):
        await self.send(dashboard_message=dashboard.DashboardActionMessages.pause)


if __name__ == "__main__":

    async def run(): ...

    asyncio.run(run())
