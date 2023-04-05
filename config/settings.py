import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR_NAME = 'temp'

# URL репозитория для скачивания файлов (только репозитории gitea).
URL = 'https://gitea.radium.group/radium/project-configuration'

# Корневой URL - применяется при формировании полных URL.
ROOT_URL: str = re.match(r'^(https:\/\/)?([\w\.]+)', URL)[0]

# Размер чанка - применяется при сохранении файлов на диск.
CHUNK_SIZE = 1024
