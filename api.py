import asyncio
from datetime import datetime
from graphene import ObjectType, String, Schema, Field

from main import track_channel, get_msg_count_per_sec


# All schema require a query.
class Query(ObjectType):
    hello = String()

    def resolve_hello(root, info):
        return 'Hello, world!'

class Subscription(ObjectType):
    time_of_day = Field(String)

    async def subscribe_time_of_day(root, info):
        while True:
            yield {'time_of_day': get_msg_count_per_sec("x2twins")}
            await asyncio.sleep(0.1)

SCHEMA = Schema(query=Query, subscription=Subscription)

async def main(schema):

    subscription = 'subscription { timeOfDay }'
    result = await schema.subscribe(subscription)
    async for item in result:
        print(item.data['timeOfDay'], datetime.now().strftime("%b %d %Y %H:%M:%S"))

track_channel("x2twins")
asyncio.run(main(SCHEMA))