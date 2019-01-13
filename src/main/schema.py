import asyncio
import graphene
import urllib.request
import xml.etree.ElementTree
import graphene.relay as relay

API_ROOT = 'https://www.goodreads.com'

async def fetch_author(id, api_key):
    file_ptr = urllib.request.urlopen(f"{API_ROOT}/author/show.xml?id={id}&key={api_key}")
    author_xml = xml.etree.ElementTree.parse(file_ptr).getroot()
    name = author_xml.findall('author')[0].findall('name')[0].text
    return Author(id=id, name=name)

class Author(graphene.ObjectType):
    id = graphene.Int(description="The author's ID.")
    name = graphene.String(description="The name of the author.")


class Query(graphene.ObjectType):
    author = graphene.Field(Author, id=graphene.Int())

    async def resolve_author(self, info, id):
        return await fetch_author(id=id, api_key=info.context['api_key'])

schema = graphene.Schema(query=Query)