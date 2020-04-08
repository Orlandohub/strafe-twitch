import os

from aiohttp import web
from tartiflette_aiohttp import register_graphql_handlers

from .twitch_chat_tracker import track_channel

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    track_channel("peacewarlando")
    return web.Response(text="Hello, world")

def run() -> None:
    """
    Entry point of the application.
    """

    app = web.Application()
    # track_channel("myth")
    app.add_routes(routes)
    web.run_app(
        register_graphql_handlers(
            app=app,
            engine_sdl=os.path.dirname(os.path.abspath(__file__)) + "/sdl",
            engine_modules=[
                "strafe_twitch.query_resolvers",
                "strafe_twitch.subscription_resolvers",
            ],
            executor_http_endpoint="/graphql",
            executor_http_methods=["POST"],
            graphiql_enabled=True,
            subscription_ws_endpoint="/ws",
        )
    )
    
