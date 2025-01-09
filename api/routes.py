from sanic import Blueprint, Request, response
from .db import drop_db

api = Blueprint("api", url_prefix="/")


@api.get("/drop_all")
async def drop_all(request: Request):
    await drop_db(request.app)
    return response.HTTPResponse(status=204)


@api.get("/")
async def index(_):
    return response.json({"response": "hello world!"})


@api.get("/ping")
async def ping(_):
    return response.json({"response": "pong"})
