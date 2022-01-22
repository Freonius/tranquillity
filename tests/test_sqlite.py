def test_sqlite():
    from ..src.settings import Sqlite

    s = Sqlite()
    s.set('test', 'val')
    _l = s._connection.execute(
        f'SELECT {s._val_col} FROM {s._tbl} WHERE {s._key_col}=?', ('test',)).fetchall()
    assert len(_l) == 1
    assert _l[0][0] == 'val'
    s.set('test', 'lav')
    _l = s._connection.execute(
        f'SELECT {s._val_col} FROM {s._tbl} WHERE {s._key_col}=?', ('test',)).fetchall()
    assert len(_l) == 1
    assert _l[0][0] == 'lav'
    assert s.is_connected is True
    s.close()
    assert s.is_connected is False
    s.connect()
    assert s.is_connected is True
    assert s['test'] == 'lav'
