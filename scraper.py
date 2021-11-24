import asyncio
from urllib.parse import urljoin
from typing import List

import aiohttp
from aiohttp.client import request
from parsel import Selector


class ScrapingException(Exception):
    pass


def normalize_url(host: str, path: str) -> str:
    """
    Converts relative urls to absolute urls. Example: /image.png -> https://example.com/image.png
    """
    return urljoin(host, path)


async def get_image_urls(url: str) -> List[str]:
    """
    :param url: URL of the website to scrape
    :return: List of image urls found in the website
    :raises ScrapingException: If any exception occurs, it is reraised as ScrapingException
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()

                html = Selector(text=text)

                image_urls = html.css('img::attr(src)').getall()

                return [normalize_url(host=url, path=image_url) for image_url in image_urls]
    except Exception as e:
        raise ScrapingException() from e


def get_image_urls_sync(url: str) -> List[str]:
    """
    :param url: URL of the website to scrape
    :return: List of image urls found in the website
    :raises ScrapingException: If any exception occurs, it is reraised as ScrapingException
    """
    try:
        response = request.get(url)
        text = response.text

        html = Selector(text=text)

        image_urls = html.css('img::attr(src)').getall()

        return [normalize_url(host=url, path=image_url) for image_url in image_urls]
    except Exception as e:
        raise ScrapingException() from e
