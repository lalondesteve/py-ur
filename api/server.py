from sanic import Sanic, Blueprint
from contextvars import ContextVar
from sanic.log import logger

from api.db import get_async_session, add_db_engine
from api.robot_api import robot_api
from api.routes import api


def create_app():
    app = Sanic("py_ur")
    routes = Blueprint.group(api, robot_api)
    app.blueprint(routes)

    _base_model_session_ctx = ContextVar("session")

    @app.before_server_start
    async def before_server_start(app):
        await add_db_engine(app)

    @app.middleware("request")
    async def inject_session(request):
        request.ctx.session = get_async_session(app.ctx.DB)
        request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx)
        logger.debug(f"{request.ctx.session_ctx_token=}")

    @app.middleware("response")
    async def close_session(request, _):
        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        logger.debug(f"closing session {request.ctx.session_ctx_token=}")
        request.ctx.session = None

    return app
