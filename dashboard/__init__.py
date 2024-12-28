import asyncio
from .dashboard_robot import check_connection, send_message
from .datatypes import DashboardMessages


if __name__ == "__main__":

    async def run():
        ip = "lals-t1.netbird.cloud"
        print(await check_connection(ip))
        print(await send_message(ip, DashboardMessages.robot_mode))

    asyncio.run(run())
