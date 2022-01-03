from ._docker import docker_ip, docker_services, docker_compose_file, docker_compose_project_name, docker_cleanup
from pytest import fixture
from _pytest.tmpdir import TempdirFactory


@fixture(scope='session')
def fld(tmpdir_factory: TempdirFactory, http_service):
    from os import chdir
    fld = tmpdir_factory.mktemp('test')
    fn = fld.join('tranquillity.yml')
    YAML = f'''
app:
  name: Tranquillity
conn:
  elasticsearch:
    host: {http_service}
    port: 9200

log:
  rotation:
    enabled: true
    daily: false
    size: 100k
    keep: 10
  loggers:
    stream:
      enabled: true
      level: debug
    file:
      enabled: true
      level: debug
      file: ./logs/{{app.name}}.log
    elasticsearch:
      level: info
      index: logs
      enabled: true
    sql:
      type: postgres
      enabled: false
      db: tq
      table: logs
      schema: tranquillity
'''
    with open(fn, 'w') as fh:
        fh.write(YAML)
    chdir(fld)
    return fld


def is_responsive(url):
    from requests import get
    try:
        response = get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@fixture(scope="session")
def http_service(docker_ip, docker_services):
    from time import sleep
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    sleep(25.)
    port = docker_services.port_for("elastic", 9200)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=60.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return str(docker_ip)
