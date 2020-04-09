import asyncio
from datetime import datetime
from typing import Any, AsyncGenerator, Dict, Optional

from tartiflette import Subscription
from .pony_db import (
    query_message_per_second,
    query_message_per_minute,
    query_kappa_per_minute
)


@Subscription("Subscription.messagesPerSecond")
async def subscribe_subscription_messages_per_second(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> AsyncGenerator[Dict[str, Any], None]:

    channel_id = args["channel"]
    while True:
        yield {
            "messagesPerSecond": query_message_per_second(channel_id)
        }
        await asyncio.sleep(0.1)


@Subscription("Subscription.messagesPerMinute")
async def subscribe_subscription_messages_per_minute(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> AsyncGenerator[Dict[str, Any], None]:

    channel_id = args["channel"]
    while True:
        yield {
            "messagesPerMinute": query_message_per_minute(channel_id)
        }
        await asyncio.sleep(0.1)


@Subscription("Subscription.kappaPerMinute")
async def subscribe_subscription_kappa_per_minute(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> AsyncGenerator[Dict[str, Any], None]:

    channel_id = args["channel"]
    while True:
        yield {
            "kappaPerMinute": query_kappa_per_minute(channel_id)
        }
        await asyncio.sleep(0.3)