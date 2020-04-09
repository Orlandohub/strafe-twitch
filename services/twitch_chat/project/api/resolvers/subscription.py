"""
TODO:
    Extra logic to check if channel exists on Twitch API or if
    the user already subscribed to it
"""

import asyncio
from datetime import datetime
from typing import Any, AsyncGenerator, Dict, Optional

from tartiflette import Subscription
from ..pony_db import (
    query_message_per_second,
    query_message_per_minute,
    query_kappa_per_minute,
)


@Subscription("Subscription.messagesPerSecond")
async def subscribe_subscription_messages_per_second(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Subscription in charge of generating an event stream related to the
    messages per second on a channels chat
    :param parent: initial value filled in to the engine `subscribe` method
    :param args: computed arguments related to the subscription
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: an asynchronous generator of the messages per second
    :rtype: Dict[str, Any]
    """

    channel_id = args["channel"]

    while True:
        yield {"messagesPerSecond": query_message_per_second(channel_id)}
        await asyncio.sleep(0.1)


@Subscription("Subscription.messagesPerMinute")
async def subscribe_subscription_messages_per_minute(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Subscription in charge of generating an event stream related to the
    messages per minute on a channels chat
    :param parent: initial value filled in to the engine `subscribe` method
    :param args: computed arguments related to the subscription
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: an asynchronous generator of the messages per minute
    :rtype: Dict[str, Any]
    """

    channel_id = args["channel"]

    while True:
        yield {"messagesPerMinute": query_message_per_minute(channel_id)}
        await asyncio.sleep(0.1)


@Subscription("Subscription.kappaPerMinute")
async def subscribe_subscription_kappa_per_minute(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Subscription in charge of generating an event stream related to the
    Kappa per minute on a channels chat
    :param parent: initial value filled in to the engine `subscribe` method
    :param args: computed arguments related to the subscription
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: an asynchronous generator of the Kappa per minute
    :rtype: Dict[str, Any]
    """

    channel_id = args["channel"]
    while True:
        yield {"kappaPerMinute": query_kappa_per_minute(channel_id)}
        await asyncio.sleep(0.3)
