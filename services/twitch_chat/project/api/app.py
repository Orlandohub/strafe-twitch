import os

from aiohttp import web
from tartiflette_aiohttp import register_graphql_handlers

from .twitch_chat_tracker import track_channel
from .pony_db import init_subscriptions


def run() -> None:
    """
    Entry point of the application.
    """

    app = web.Application()
    app.on_startup.append(init_subscriptions)

    web.run_app(
        register_graphql_handlers(
            app=app,
            engine_sdl=os.path.dirname(os.path.abspath(__file__)) + "/sdl",
            engine_modules=[
                "project.api.resolvers.query",
                "project.api.resolvers.subscription",
                "project.api.resolvers.mutation",
            ],
            executor_http_endpoint="/graphql",
            executor_http_methods=["POST"],
            graphiql_enabled=True,
            subscription_ws_endpoint="/ws",
        )
    )
