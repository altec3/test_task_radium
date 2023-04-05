import pytest

from modules.utils import split_list


class TestSplitList:

    @pytest.mark.parametrize('lst, item_count', [
        ([1, 2, 3, 4], 3),
        ([1, 2, 3], 3),
        ([1, 2], 3)
    ])
    def test_not_empty_list(self, lst, item_count):
        items = len(lst)
        if items < item_count:
            for item in split_list(lst, item_count):
                assert len(item) == items
        elif items % item_count > 0:
            for item in split_list(lst, item_count):
                if len(item) == item_count:
                    continue
                assert len(item) == items % item_count
        else:
            for item in split_list(lst, item_count):
                assert len(item) == item_count

    def test_empty_list(self):
        for item in split_list([]):
            assert item is None
