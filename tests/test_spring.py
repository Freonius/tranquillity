def test_spring(http_service):
    from ..src.settings import SpringConfig
    s = SpringConfig(http_service, 'application', 'foo')
    assert s['name'] == 'master'
    s = SpringConfig(f'http://{http_service}', 'application', 'foo')
    assert s['name'] == 'master'
    s = SpringConfig(f'http://{http_service}:8888', 'application', 'foo')
    assert s['name'] == 'master'
    s = SpringConfig(f'{http_service}:8888', 'application', 'foo')
    assert s['name'] == 'master'
