from typing import Any, Dict, List, Optional

from tartiflette import Resolver


@Resolver("Query.hello")
async def resolver_hello(parent, args, ctx, info):
    return "hello " + args["name"]
