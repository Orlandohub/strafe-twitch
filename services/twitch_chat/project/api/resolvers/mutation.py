from typing import Any, Dict, Optional

from tartiflette import Resolver

from ..twitch_chat_tracker import track_channel


@Resolver("Mutation.trackChannel")
async def resolve_mutation_track_channel(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> Dict[str, Any]:
    """
    Resolver in charge of the mutation to subscribe to a channel.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the mutation
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: the mutated channel ID with success message
    :rtype: Dict[str, Any]
    """
    channel = args["channel"]
    tracking_channel = track_channel(channel)

    if tracking_channel:
        return "Successfuly tracking " + args["channel"]

    return "This channel does not exist on Twitch or was already subscribed to!"
