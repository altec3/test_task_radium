import hashlib


def split_list(lst: list, item_count: int = 3) -> list:
    """
    Разбивает список на списки с определенным количеством элементов.

    :param lst: Список, который необходимо разделить
    :param item_count: Количество элементов,
                       которое необходимо оставить в списке
    :return: Список с количеством элементов равным item_count
    """
    try:
        for element in range(0, len(lst), item_count):
            element_list = lst[element: item_count + element]

            yield element_list
    except TypeError as exception:
        print('[split_list]', exception)


def compute_file_hash(path: str) -> str:
    """
    Вычисляет sha256 хэш файла.

    :param path: Путь до файла
    :return: Вычисленный хэш
    """
    with open(path, 'rb') as file_stream:
        hsh = hashlib.sha256()
        while True:
            file_data: bytes = file_stream.read(2048)
            if not file_data:
                break
            hsh.update(file_data)
        return hsh.hexdigest()
