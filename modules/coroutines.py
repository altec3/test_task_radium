import time
from pathlib import Path

from aiohttp import ClientSession, client_exceptions
from bs4 import BeautifulSoup, element

from config.settings import ROOT_URL, CHUNK_SIZE


async def get_files_page_url(session: ClientSession, url: str) -> str | None:
    """Получает URL страницы со списком файлов репозитория."""
    try:
        async with session.get(url, raise_for_status=True) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            tags: list[element.Tag] = soup.find_all(
                class_='ui compact basic button tooltip'
            )
            for tag in tags:
                if tag.attrs.get('data-content') == 'Go to file':
                    url: str = tag.attrs.get('href')
                    if not url:
                        print('[get_files_page_url]: URL not found')
                        exit(1)
                    return '{0}{1}'.format(ROOT_URL, url)
    except (TypeError,
            client_exceptions.ClientConnectionError,
            client_exceptions.ClientResponseError,
            ) as exception:
        print('[get_files_page_url]', exception)


async def get_download_links(session: ClientSession, url: str) -> list | None:
    """ Получает список ссылок на файлы репозитория """
    data_urls = {}
    try:
        async with session.get(url, raise_for_status=True) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            tags: list[element.Tag] = soup.find_all('input')
            for tag in tags:
                if not tag.attrs.get('data-url-data-link') or not tag.attrs.get('data-url-tree-link'):
                    continue
                data_urls['data-url-data-link'] = '{0}{1}'.format(ROOT_URL, tag.attrs.get('data-url-data-link'))
                data_urls['data-url-tree-link'] = '{0}{1}/'.format(ROOT_URL, tag.attrs.get('data-url-tree-link'))

        # Получим список имен файлов, находящихся в репозитории
        async with session.get(data_urls['data-url-data-link'], raise_for_status=True) as resp:
            file_list: list = await resp.json()

            # Получим список ссылок на файлы, находящихся в репозитории
            file_links = [data_urls['data-url-tree-link'] + filename for filename in file_list]
            return list(map(lambda l: l.replace('/src/', '/raw/', 1), file_links))
    except (TypeError,
            client_exceptions.ClientConnectionError,
            client_exceptions.ClientResponseError,
            ) as exception:
        print('[get_download_links]', exception)


async def download_file(session: ClientSession, link: str, output_dir: Path) -> tuple | None:
    """ Загружает файл """
    try:
        async with session.get(link, raise_for_status=True) as response:
            filename = link.split('/')[-1]
            save_path = output_dir.resolve().joinpath(filename)
            if not (save_path.exists() and save_path.is_file()):
                with open(save_path, 'wb') as fd:
                    async for chunk in response.content.iter_chunked(CHUNK_SIZE):
                        fd.write(chunk)
                print(time.strftime('%X'), 'File saved as {0} in {1}'.format(filename, output_dir))
                return filename, save_path
    except (TypeError,
            client_exceptions.ClientConnectionError,
            client_exceptions.ClientResponseError,
            ) as exception:
        print('[download_file]', exception)
