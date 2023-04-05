### Тестовое задание
*Стек: python:3.10*  
*Среда разработки: PyCharm*

---
### Описание задания

Скрипт асинхронно (в 3 одновременные задачи) скачивает содержимое HEAD репозитория
https://gitea.radium.group/radium/project-configuration во временную папку.
После выполнения всех асинхронных задач, скрипт подсчитывает sha256 хэши от каждого файла.

---

#### Для проверки задания (IDE PyCharm):

1. При необходимости, изменить настройки в файле [settings.py](./config/settings.py)
2. Установить зависимости:
```python
pip install poetry
poetry install
```
3. Запустить скрипт:
```python
python run.py
```
В результате во временную папку будут скачаны все файлы из указанного в [settings.py](./config/settings.py) репозитория
(по умолчанию https://gitea.radium.group/radium/project-configuration).

#### Запуск тестов (IDE PyCharm)
```python
pytest
```
