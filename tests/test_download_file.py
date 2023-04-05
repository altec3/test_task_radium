import os
from pathlib import Path
from aiohttp import ClientSession

from modules.coroutines import download_file

link = 'https://gitea.radium.group/radium/project-configuration/raw/branch/master/README.md'
output_dir = Path(__file__).resolve().parent


class TestDownloadFile:

    async def test_valid_url(self, loop):
        async with ClientSession() as session:
            filename, path = await download_file(session, link, output_dir)
            os.remove(path)
        assert isinstance(filename, str)

    async def test_invalid_url(self, loop):
        async with ClientSession() as session:
            filename = await download_file(session, link[:10], output_dir)
        assert filename is None
