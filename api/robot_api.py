from pydantic import ValidationError
from sanic import Blueprint
from sanic.request import Request
from sanic_ext import openapi
import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sanic.response import json
from sanic.log import logger
from .schema import RobotConfig, RobotConfigUpdate, RobotConfigFromDb
from .models import RobotConfigModel

robot_api = Blueprint("robot_api", url_prefix="/robot")


@robot_api.get("/")
async def get_robot(request):
    robots = None
    async for conn in request.ctx.session:
        robot_model = sqlalchemy.select(RobotConfigModel)
        robots = await conn.execute(robot_model)

        robots = [
            RobotConfigFromDb.model_validate(robot) for robot in robots.scalars().all()
        ]
    if robots:
        return json([robot.model_dump(mode="json") for robot in robots])
    return json({})


@robot_api.get("/<_id:int>")
async def get_robot_by_id(request, _id):
    robot = None
    robot_model = sqlalchemy.select(RobotConfigModel).where(RobotConfigModel.id == _id)
    try:
        async for conn in request.ctx.session:
            value = await conn.execute(robot_model)
            robot = RobotConfigFromDb.model_validate(value.scalars().one())
    except Exception as e:
        logger.error(repr(e), e)
    else:
        if robot:
            return json(robot.model_dump(mode="json"))
    return json(status=404, body={"error": "ID not found"})


@robot_api.post("/")
@openapi.definition(body={"application/json": RobotConfig.model_json_schema()})
async def create_robot(request: Request):
    data = request.json
    robot_from_db = None
    try:
        robot_config = RobotConfig.model_validate(data)
        async for conn in request.ctx.session:
            robot_model = RobotConfigModel(**robot_config.model_dump(mode="json"))
            conn.add(robot_model)
            await conn.commit()
            await conn.refresh(robot_model)
            robot_from_db = RobotConfigFromDb.model_validate(robot_model)
    except ValidationError:
        return json(status=403, body={"error": "Invalid data"})
    except IntegrityError:
        return json(status=403, body={"error": "IP address already exists"})
    except Exception as e:
        print(f"Error: {e}")
        logger.error(repr(e), e)
        return json(status=400, body={"error": repr(e)})
    else:
        if robot_from_db:
            return json(status=200, body=robot_from_db.model_dump(mode="json"))
    return json(status=404, body={"error": "Robot not created"})


@robot_api.put("/<_id:int>")
@openapi.definition(body={"application/json": RobotConfigUpdate.model_json_schema()})
async def update_robot(request, _id):
    data = request.json
    robot_from_db = None
    try:
        robot_update = RobotConfigUpdate.model_validate(data)
    except ValidationError:
        return json(status=403, body={"error": "Invalid data"})
    try:
        async for conn in request.ctx.session:
            robot_model = (
                sqlalchemy.update(RobotConfigModel)
                .where(RobotConfigModel.id == _id)
                .values(robot_update.model_dump(mode="json"))
            )
            await conn.execute(robot_model)
            await conn.commit()
            get_robot_from_db = sqlalchemy.select(RobotConfigModel).where(
                RobotConfigModel.id == _id
            )
            robot_from_db = RobotConfigFromDb.model_validate(
                (await conn.execute(get_robot_from_db)).scalars().one()
            )

    except Exception as e:
        logger.error(repr(e), e)
        return json(status=400, body={"error": repr(e)})
    else:
        if robot_from_db:
            return json(status=200, body=robot_from_db.model_dump(mode="json"))

    return json(status=404, body={"error": "Robot not created"})


@robot_api.delete("/<_id:int>")
async def delete_robot(request: Request, _id):
    try:
        async for conn in request.ctx.session:
            robot = sqlalchemy.delete(RobotConfigModel).where(
                RobotConfigModel.id == _id
            )
            await conn.execute(robot)
            await conn.commit()
    except Exception as e:
        logger.error(repr(e), e)
        return json(status=400, body={"error": repr(e)})
    else:
        return json(status=200, body={"response": f"Robot with id {_id} deleted"})


@robot_api.get("/<_id:int>/state")
async def get_robot_state(request, _id):
    return json(status=204, body={})
