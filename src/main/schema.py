import asyncio
import graphene
import urllib.request
import xml.etree.ElementTree
import graphene.relay as relay

API_ROOT = 'https://www.goodreads.com'

async def fetch_xml(url):
    file_ptr = urllib.request.urlopen(url)
    return xml.etree.ElementTree.parse(file_ptr).getroot()

class Author(graphene.ObjectType):
    id = graphene.Int(description="The author's ID.")
    name = graphene.String(description="The name of the author.")
    
    @staticmethod
    def resolve_id(xml, info):
        return xml.findall('id')[0].text

    @staticmethod
    def resolve_name(xml, info):
        return xml.findall('name')[0].text

class Query(graphene.ObjectType):
    author = graphene.Field(Author, id=graphene.Int(), description='An author.')
    
    @staticmethod
    async def resolve_author(_, info, id):
        xml = await fetch_xml(f"{API_ROOT}/author/show.xml?id={id}&key={info.context['api_key']}")
        return xml.findall('author')[0]

schema = graphene.Schema(query=Query)