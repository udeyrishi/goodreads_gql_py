# Copyright (c) 2019 Udey Rishi. All rights reserved.

import logging
import requests
from xml.etree import ElementTree

class GoodReadsXMLApi:
    __API_ROOT = 'https://www.goodreads.com'

    def __init__(self, api_key):
        self.__api_key = api_key

    async def get_author(self, id):
        return await self.__fetch_xml(resource='author', id=id)

    async def get_book(self, id):
        return await self.__fetch_xml(resource='book', id=id)

    async def __fetch_xml(self, resource, id):
        logging.getLogger(type(self).__name__).debug(f'Fetching {resource} with id: {id}')
        
        url = f"{self.__API_ROOT}/{resource}/show.xml?id={id}&key={self.__api_key}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return ElementTree.fromstring(response.content).findall(resource)[0]
        elif response.status_code == 404:
            return None
        else:
            raise ValueError(f'Received unexpected error code {response.status_code} from Goodreads API.')