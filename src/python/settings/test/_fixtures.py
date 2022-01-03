from ._docker import docker_ip, docker_services, docker_compose_file, docker_compose_project_name, docker_cleanup
from pytest import fixture
from _pytest.tmpdir import TempdirFactory


@fixture(scope='session')
def fld(tmpdir_factory: TempdirFactory):
    fld = tmpdir_factory.mktemp('test')
    fn = fld.join('tranquillity.yml')
    JSON = '''
    { "value": { "value": 2 } }
    '''
    INI = '''
[app]
name = Tranquillity
'''
    YAML = '''
app:
  name: Tranquillity
conn:
  mongo:
    host: mongo
    port: 1234
mylist:
  - 1
  - 2
  - 3
abool: true
notabool: 1
'''
    with open(fn, 'w') as fh:
        fh.write(YAML)
    with open(fld.join('settings.yaml'), 'w') as fh:
        fh.write(YAML)
    with open(fld.join('settings.json'), 'w') as fh:
        fh.write(JSON)
    with open(fld.join('another.yml'), 'w') as fh:
        fh.write('')
    with open(fld.join('3.yml'), 'w') as fh:
        fh.write('')
    with open(fld.join('4.yml'), 'w') as fh:
        fh.write('')
    with open(fld.join('settings.properties'), 'w') as fh:
        fh.write(INI)
    with open(fld.join('settings.ini'), 'w') as fh:
        fh.write(INI)
    return str(fld)


def is_responsive(url):
    from requests import get
    try:
        response = get(url)
        if response.status_code == 404:
            return True
    except ConnectionError:
        return False


@fixture(scope="session")
def http_service(docker_ip, docker_services):
    from time import sleep
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    sleep(25.)
    port = docker_services.port_for("spring", 8888)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=60.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return str(docker_ip)
