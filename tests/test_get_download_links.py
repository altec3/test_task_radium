from aiohttp import ClientSession

from modules.coroutines import get_download_links

url = 'https://gitea.radium.group/radium/project-configuration/find/branch/master'


class TestGetDownloadLinks:

    async def test_valid_url(self, loop):
        async with ClientSession() as session:
            download_links = await get_download_links(session, url)
        assert isinstance(download_links, list)

    async def test_url_is_none(self, loop):
        async with ClientSession() as session:
            download_links = await get_download_links(session, None)
        assert download_links is None
