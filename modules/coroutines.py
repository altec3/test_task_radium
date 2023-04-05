import time
from pathlib import Path

from aiohttp import ClientSession, client_exceptions
from bs4 import BeautifulSoup, element

from config.settings import ROOT_URL, CHUNK_SIZE


async def get_files_page_url(session: ClientSession, url: str):
    try:
        async with session.get(url, raise_for_status=True) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            tags: list[element.Tag] = soup.find_all(class_='ui compact basic button tooltip')
            for tag in tags:
                if tag.attrs.get('data-content') == 'Go to file':
                    url: str = tag.attrs.get('href')
                    if not url:
                        print('[get_files_page_url]: URL not found')
                        exit(1)
                    return ROOT_URL + url
    except (TypeError,
            client_exceptions.ClientConnectionError,
            client_exceptions.ClientResponseError,
            ) as e:
        print('[get_files_page_url]', e)


async def get_download_links(session: ClientSession, url: str):
    data_urls = {}
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print('[get_download_links]: The request failed. Check url address or try again later')
                exit(1)

            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            tags: list[element.Tag] = soup.find_all('input')
            for tag in tags:
                if not tag.attrs.get('data-url-data-link') or not tag.attrs.get('data-url-tree-link'):
                    continue
                data_urls['data-url-data-link'] = ROOT_URL + tag.attrs.get('data-url-data-link')
                data_urls['data-url-tree-link'] = ROOT_URL + tag.attrs.get('data-url-tree-link') + '/'

        # Получим список имен файлов, находящихся в репозитории
        async with session.get(data_urls['data-url-data-link']) as resp:
            if resp.status != 200:
                print('[get_download_links]: The request failed.')
                exit(1)

            file_list: list = await resp.json()

            # Получим список ссылок на файлы, находящихся в репозитории
            file_links = [data_urls['data-url-tree-link'] + filename for filename in file_list]
            return list(map(lambda l: l.replace('/src/', '/raw/', 1), file_links))
    except (TypeError,
            client_exceptions.ClientConnectionError,
            client_exceptions.ClientResponseError,
            ) as e:
        print('[get_download_links]', e)


async def download_file(session: ClientSession, link: str, output_dir: Path):
    try:
        async with session.get(link, raise_for_status=True) as response:
            filename = link.split('/')[-1]
            save_path = output_dir.resolve().joinpath(filename)
            if not (save_path.exists() and save_path.is_file()):
                with open(save_path, 'wb') as fd:
                    async for chunk in response.content.iter_chunked(CHUNK_SIZE):
                        fd.write(chunk)
                print(time.strftime('%X'), f'File saved as {filename} in {output_dir}')
                return filename, save_path
    except (TypeError,
            client_exceptions.ClientConnectionError,
            client_exceptions.ClientResponseError,
            ) as e:
        print(f'[download_file]', e)
