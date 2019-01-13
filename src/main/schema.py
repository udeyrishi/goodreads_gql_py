import asyncio
import graphene
import requests
from xml.etree import ElementTree

API_ROOT = 'https://www.goodreads.com'

async def fetch_xml(url):
    response = requests.get(url)
    if response.status_code == 200:
        return ElementTree.fromstring(response.content)
    elif response.status_code == 404:
        return None
    else:
        raise ValueError(f'Received unexpected error code {response.status_code} from Goodreads API.')

class Book(graphene.ObjectType):
    title = graphene.NonNull(
        graphene.String, 
        description="The title of the book.", 
        resolver=lambda xml, info: xml.findall('title')[0].text
    )

    isbn = graphene.String(
        description="The ISBN of the book.", 
        resolver=lambda xml, info: xml.findall('isbn')[0].text
    )
    
    isbn13 = graphene.String(
        description="The ISBN13 of the book.", 
        resolver=lambda xml, info: xml.findall('isbn13')[0].text
    )

class Author(graphene.ObjectType):
    id = graphene.NonNull(
        graphene.Int, 
        description="The author's ID.", 
        resolver=lambda xml, info: int(xml.findall('id')[0].text)
    )
    
    name = graphene.NonNull(
        graphene.String, 
        description="The name of the author.", 
        resolver=lambda xml, info: xml.findall('name')[0].text
    )
    
    books = graphene.NonNull(
        graphene.List(Book), 
        resolver=lambda xml, info: xml.findall('books')[0].findall('book')
    )

class Query(graphene.ObjectType):
    author = graphene.Field(Author, id=graphene.NonNull(graphene.Int), description='An author.')
    
    @staticmethod
    async def resolve_author(_, info, id):
        xml = await fetch_xml(f"{API_ROOT}/author/show.xml?id={id}&key={info.context['api_key']}")
        return None if xml is None else xml.findall('author')[0]

schema = graphene.Schema(query=Query)