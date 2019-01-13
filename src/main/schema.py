import asyncio
import graphene


class Query(graphene.ObjectType):
    hello = graphene.String(argument=graphene.String(default_value="stranger"))

    async def resolve_hello(self, info, argument):
        await asyncio.sleep(5)
        return 'Hello ' + argument

schema = graphene.Schema(query=Query)