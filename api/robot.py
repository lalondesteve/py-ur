from schema import RobotConfigFromDb
from py_ur.robot import Robot


async def init_robot_objects(app):
    app.ctx.robots = [Robot(config) for config in app.ctx.robot_configs]


async def get_robot_object(config: RobotConfigFromDb):
    return Robot(**config.model_dump())


async def update_robot_register(RegisterEnum, robot_id):
    pass


async def read_robot_register(RegisterEnum, robot_id):
    pass
