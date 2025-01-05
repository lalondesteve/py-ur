from sanic import Blueprint, Request, response
from .db import drop_db

api = Blueprint("api", url_prefix="/")


@api.route("/drop_all")
async def drop_all(request: Request):
    await drop_db(request.app)
    return response.HTTPResponse(status=204)


@api.route("/")
async def index(_):
    return response.json({"response": "hello world!"})


@api.route("/ping")
async def ping(_):
    return response.json({"response": "pong"})
