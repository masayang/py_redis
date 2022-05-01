from pydis.redis_list import RedisList
import pytest



class TestRedisDict:
    def test_constructor_without_items(self, resource):
        l = RedisList(id="xxx")
        assert l.item_type == str

    def test_constructor_with_items(self, resource):
        l = RedisList(id="xxx", items=[1, 2, 3])
        assert l.item_type == str
        
        l = RedisList(id="xxx", item_type=int, items=[1, 2, 3])
        assert l.item_type == int

    def test_getitem_no_slice(self, resource):
        l = RedisList(id="list", item_type=int, items=[1, 2, 3])
        assert l[0] == 1
        assert l[1] == 2
        assert l[2] == 3

    def test_getitem_with_slice_no_step(self, resource):
        l = RedisList(id="list", items=[1, 2, 3])
        assert l[0:1] == ['1', '2']

    def test_getitem_with_slice_with_step_1(self, resource):
        l = RedisList(id="list", item_type=int, items=[1, 2, 3, 4, 5, 6])
        assert l[0:3:1] == [1, 2, 3, 4]

    def test_getitem_with_slice_with_step_2(self, resource):
        l = RedisList(id="list", item_type=int, items=[1, 2, 3, 4, 5, 6])
        #assert l[0:3:2] == [1, 2, 3, 4]
        with pytest.raises(NotImplementedError) as excinfo:
            l[0:3:2] == [1, 2, 3, 4]
        assert "Cannot specify a step to a RedisObject slice" in str(excinfo.value)

    def test_setitem(self, resource):
        l = RedisList(id="list", items=["", "", ""])
        l[1] = "hogehoge"
        assert l[1] == "hogehoge"

    def test_len(self, resource):
        l = RedisList(id="list", items=["", "", ""])
        assert len(l) == 3

    def test_delitem(self, resource):
        l = RedisList('list', items=['1', '2', '3'])
        del l[1]
        assert l[0] == '1'
        assert l[1] == '3'

    def test_lpop(self, resource):
        l = RedisList('list', item_type=int, items=[0, 1, 2, 3])
        assert l.lpop() == 0
        assert l[0] == 1
        assert l[1] == 2
        assert l[2] == 3
        assert len(l) == 3

    def test_rpop(self, resource):
        l = RedisList('list', item_type=int, items=[0, 1, 2, 3])
        assert l.rpop() == 3
        assert l[0] == 0
        assert l[1] == 1
        assert l[2] == 2
        assert len(l) == 3

    def test_rpush(self, resource):
        l = RedisList('list', item_type=int, items=[0, 1, 2, 3])
        l.rpush(0)
        assert l[0] == 0
        assert l[1] == 1
        assert l[2] == 2
        assert l[3] == 3
        assert l[4] == 0
        assert len(l) == 5

    def test_lpush(self, resource):
        l = RedisList('list', item_type=int, items=[0, 1, 2, 3])
        l.lpush(0)
        assert l[0] == 0
        assert l[1] == 0
        assert l[2] == 1
        assert l[3] == 2
        assert l[4] == 3
        assert len(l) == 5

    def test_append(self, resource):
        l = RedisList('list', item_type=int, items=[0, 1, 2, 3])
        l.append(0)
        assert l[0] == 0
        assert l[1] == 1
        assert l[2] == 2
        assert l[3] == 3
        assert l[4] == 0
        assert len(l) == 5

    def test_iterator(self, resource):
        l = RedisList('list', item_type=int, items=[0, 1, 2, 3])
        l2 = []
        for item in l:
            l2.append(item)
        assert l2 == [0, 1, 2, 3]

    def test_insert_before(self, resource):
        l = RedisList('list', item_type=int, items=[0, 1, 2, 3])
        l.insert_before(2, 100)
        assert l[0] == 0
        assert l[1] == 1
        assert l[2] == 100
        assert l[3] == 2
        assert l[4] == 3
        assert len(l) == 5

    def test_insert_after(self, resource):
        l = RedisList('list', item_type=int, items=[0, 1, 2, 3])
        l.insert_after(2, 100)
        assert l[0] == 0
        assert l[1] == 1
        assert l[2] == 2
        assert l[3] == 100
        assert l[4] == 3
        assert len(l) == 5

    def test_trim(self, resource):
        l = RedisList('list', item_type=int, items=[0, 1, 2, 3, 4, 5])
        l.trim(2, 3)
        assert l[0] == 2
        assert l[1] == 3
        assert len(l) == 2
