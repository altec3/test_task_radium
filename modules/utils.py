import hashlib


def split_list(lst: list, item_count: int = 3) -> list:
    """
    Разбивает список на списки с определенным количеством элементов

    :param lst: Список, который необходимо разделить
    :param item_count: Количество элементов, которое необходимо оставить в списке
    :return: Список с количеством элементов равным item_count
    """
    try:
        for item in range(0, len(lst), item_count):
            result = lst[item: item_count + item]

            yield result
    except TypeError as e:
        print('[split_list]', e)


def compute_file_hash(path: str) -> str:
    """
    Вычисляет sha256 хэш файла

    :param path: Путь до файла
    :return: Вычисленный хэш
    """
    with open(path, 'rb') as file:
        hsh = hashlib.sha256()
        while True:
            data = file.read(2048)
            if not data:
                break
            hsh.update(data)
        return hsh.hexdigest()
