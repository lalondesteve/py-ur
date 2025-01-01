import asyncio

import dashboard
import modbus
import logging
import json

logger = logging.getLogger(__name__)


class Robot:
    def __init__(self, ip: str):
        self.ip = ip
        self.online = False
        self.modbus_online = False
        self.dashboard_online = False
        self.modbus_status = dict()
        self.dashboard_status = dict()
        self.user_registers = dict()

    async def check_online(self):
        mr = mw = dr = dw = None
        try:
            async for mr, mw in modbus.connect(self.ip):
                pass
            async for dr, dw in dashboard.connect(self.ip):
                pass
        except Exception as e:
            self.online = False
            logger.debug(e)
        else:
            if not mr or mw:
                self.modbus_online = False
            else:
                self.modbus_online = True
            if not dr or dw:
                self.dashboard_online = False
            else:
                self.dashboard_online = True
            self.online = any([self.modbus_online, self.dashboard_online])
            logger.debug(f"online: {self.online}")

    async def get_modbus_status(self):
        responses = [
            modbus.resolve_register(r)
            for r in await modbus.build_and_send_messages(
                self.ip, [m for m in modbus.StatusRegister]
            )
        ]
        self.modbus_status = {response.name: response.value for response in responses}

    async def get_dashboard_status(self):
        responses = [await dashboard.send_batch_messages(self.ip, [m]) for m in dashboard.DashboardStatusMessages]
        self.dashboard_status = {
            response[0][0].name:
                self.filter_dashboard_responses(response[0][1].decode())
            for response in responses
        }

    @staticmethod
    def filter_dashboard_responses(response: str):
        if ':' in response:
            response = response.split(':')[1].strip()
        if len(words := response.split(' ')) > 1:
            response = words[0]
        try:
            response = json.loads(response)
        except json.JSONDecodeError:
            pass
        return response

    async def power_on(self):
        pass

    async def power_off(self):
        pass

    async def release_brake(self):
        pass

    async def play(self):
        pass

    async def stop(self):
        pass

    async def pause(self):
        pass


if __name__ == "__main__":
    async def run():
        r = Robot("lals-t1.netbird.cloud")
        await r.get_dashboard_status()
        print(r.dashboard_status)


    asyncio.run(run())
