from typing import Callable
from ipaddress import IPv4Address

import logging
import json

from py_ur.modbus_datatypes import RegisterEnum
from . import dashboard, modbus, DashboardActionMessages, DashboardStatusMessages

from py_ur.utils import get_ursim_ip

logger = logging.getLogger(__name__)


class Robot:
    def __init__(
        self,
        ip: str | IPv4Address = get_ursim_ip(),
        message_callback: Callable | None = None,
    ):
        self.ip = ip
        self.message_callback = message_callback
        self.online = False
        self.modbus_online = False
        self.dashboard_online = False
        self.modbus_state: dict[RegisterEnum, int] = dict()
        self.dashboard_state: dict[str, str] = dict()
        self.user_registers = dict()
        self._ip: IPv4Address

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip: str | IPv4Address):
        if isinstance(ip, str):
            ip = IPv4Address(ip)
        self._ip = ip

    async def check_online(self):
        mw = dw = None
        try:
            async with modbus.connect(self.ip.compressed) as (_, mw):
                if mw is None:
                    self.modbus_online = False
                else:
                    self.modbus_online = True
            async with dashboard.connect(self.ip.compressed) as (_, dw):
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

    async def get_modbus_state(self):
        responses = await modbus.build_and_send_messages(
            ip=self.ip.compressed,
            messages=[
                m for m in modbus.RegisterEnum if not m.name.startswith("register_")
            ],
        )
        self.modbus_state = {
            response.register: response.value for response in responses
        }

    async def get_register_status(self, registers: list[modbus.RegisterEnum]):
        print(
            await modbus.build_and_send_messages(
                ip=self.ip.compressed, messages=registers
            )
        )

    async def get_dashboard_state(self):
        responses = [
            await dashboard.send_batch_messages(ip=self.ip.compressed, messages=[m])
            for m in DashboardStatusMessages
        ]
        self.dashboard_state = {
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
                ip=self.ip.compressed, messages=dashboard_message
            )
            if callback and response:
                callback(response)

        if modbus_message:
            if not isinstance(modbus_message, list):
                modbus_message = [modbus_message]
            response = await modbus.build_and_send_messages(
                ip=self.ip.compressed, messages=modbus_message
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
        await self.send(dashboard_message=DashboardActionMessages.play)

    async def stop(self):
        await self.send(dashboard_message=DashboardActionMessages.stop)

    async def pause(self):
        await self.send(dashboard_message=DashboardActionMessages.pause)
