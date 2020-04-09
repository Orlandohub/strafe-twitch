from typing import Any, Dict, List, Optional

from tartiflette import Resolver

from .twitch_chat_tracker import track_channel


@Resolver("Query._")
async def resolver_query(parent, args, ctx, info):
    """
    Empty resolver.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the field
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: True
    :rtype: Dict[Boolean, Any]
    """
    return True
