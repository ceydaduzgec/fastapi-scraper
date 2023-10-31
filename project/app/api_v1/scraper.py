from typing import List
from urllib.parse import urljoin

import aiohttp
import requests
from app.core.constants import MAX_IMAGE_NUMBER
from parsel import Selector


class ScrapingException(Exception):
    pass


async def get_image_urls(url: str) -> List[str]:
    """
    :param url: URL of the website to scrape
    :return: List of image urls found in the website
    :raises ScrapingException: If any exception occurs, it is reraised as ScrapingException
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                text = await response.text()
                html = Selector(text=text)
                image_urls = html.css("img::attr(src)").getall()
                # Limit the number of images to MAX_IMAGE_NUMBER
                image_urls = image_urls[:MAX_IMAGE_NUMBER]
                return [urljoin(base=url, url=image_url) for image_url in image_urls]

    except Exception as e:
        raise ScrapingException() from e


def get_image_urls_sync(url: str) -> List[str]:
    """
    :param url: URL of the website to scrape
    :return: List of image urls found in the website
    :raises ScrapingException: If any exception occurs, it is reraised as ScrapingException
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
        html = Selector(text=text)
        image_urls = html.css("img::attr(src)").getall()
        # Limit the number of images to MAX_IMAGE_NUMBER
        image_urls = image_urls[:MAX_IMAGE_NUMBER]
        return [urljoin(base=url, url=image_url) for image_url in image_urls]
    except Exception as e:
        raise ScrapingException() from e
