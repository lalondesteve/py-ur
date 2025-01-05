from schema import RobotConfigFromDb
from py_ur.robot import Robot


async def init_robot_objects(app):
    pass


async def get_robot_object(config: RobotConfigFromDb):
    return Robot(**config.model_dump())


async def update_robot_register(RegisterEnum, robot_id):
    pass


async def read_robot_register(RegisterEnum, robot_id):
    pass
