import asyncio
import os
from aiohttp import ClientSession

from config.settings import URL, BASE_DIR, TEMP_DIR_NAME
from modules.coroutines import get_files_page_url, get_download_links, download_file
from modules.utils import split_list, compute_file_hash


async def main(url: str):
    if 'gitea.' not in url:
        print('[main]: This script for "gitea" repositories only')
        exit(1)

    session = ClientSession()
    downloaded_files = []
    temp_dir = BASE_DIR.resolve().joinpath(TEMP_DIR_NAME)

    if not temp_dir.exists():
        os.mkdir(temp_dir)

    if downloaded_files:
        downloaded_files.clear()

    async with session:
        # Получим URL странички со списком всех файлов репозитория
        page_url = await get_files_page_url(session=session, url=url)

        # Получим список ссылок для загрузки файлов
        download_links = await get_download_links(session=session, url=page_url)

        # Скачаем файлы (по умолчанию, макс. 3 задачи)
        for links in split_list(download_links):
            tasks = [asyncio.create_task(download_file(session=session, link=link, output_dir=temp_dir)) for link in links]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    downloaded_files.append(result)

    # Без данной задержки выполнение асинхронной части скрипта заканчивается с ошибкой:
    # 'RuntimeError: Event loop is closed'
    await asyncio.sleep(0.5)

    # Вычислим sha256 хэши от каждого файла
    if downloaded_files:
        print('===== Computed hashes of files ======')
        for filename, path in downloaded_files:
            print(filename, '[sha256]', compute_file_hash(path))


if __name__ == '__main__':
    asyncio.run(main(URL))
