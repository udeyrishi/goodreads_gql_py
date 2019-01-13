from aiodataloader import DataLoader
import asyncio
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

async def fetch_author_xml(id, api_key):
    xml = await fetch_xml(f"{API_ROOT}/author/show.xml?id={id}&key={api_key}")
    return None if xml is None else xml.findall('author')[0]

class AuthorXMLLoader(DataLoader):
    def __init__(self, *args, **kwargs):
        if 'api_key' in kwargs:
            self.__api_key = kwargs['api_key']
            del kwargs['api_key']
        else:
            raise ValueError('api_key must be provided as a key-value ark to AuthorXMLLoader.')
        super(AuthorXMLLoader, self).__init__(*args, **kwargs)

    async def batch_load_fn(self, keys):# pylint: disable=E0202
        tasks = [asyncio.create_task(fetch_author_xml(id=id, api_key=self.__api_key)) for id in keys]
        return [await task for task in tasks]