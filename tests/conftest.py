import pytest

pytest_plugins = 'aiohttp.pytest_plugin'


@pytest.fixture()
def url() -> str:
    return 'https://gitea.radium.group/radium/project-configuration'
