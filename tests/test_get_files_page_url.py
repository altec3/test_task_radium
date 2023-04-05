from aiohttp import ClientSession

from modules.coroutines import get_files_page_url

url = 'https://gitea.radium.group/radium/project-configuration'


class TestGetFilesPageUrl:

    async def test_valid_url(self, loop):
        async with ClientSession() as session:
            response = await get_files_page_url(session, url)
        assert isinstance(response, str)

    async def test_invalid_url(self, loop):
        async with ClientSession() as session:
            response = await get_files_page_url(session, url[:9])
        assert response is None
