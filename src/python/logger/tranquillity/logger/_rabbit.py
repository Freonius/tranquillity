from typing import Union, Callable, Set
from pickle import dumps
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from tranquillity.settings import ISettings
from tranquillity.exceptions import ConnectionException
from .__interfaces import ILogHandler
from .__custom_log_record import CustomLogRecord, _lr2d


class RabbitLogHandler(ILogHandler):
    _queue: str
    _client: BlockingConnection
    _channel: BlockingChannel

    def __init__(self, settings: ISettings):
        super().__init__(settings)
        self.initialize_client()

    # @staticmethod
    def initialize_client(self) -> None:
        _ks: Callable[[str], Set[str]] = lambda x: {
            x,
            f'rabbitmq.{x}',
            f'conns.rabbitmq.{x}',
            f'rabbit.{x}',
            f'conn.rabbit.{x}',
        }
        _host: Union[str, None] = self._settings.lookup(_ks('host'))
        if _host is None:
            raise ConnectionException('host is not defined')
        _port: int = int(str(self._settings.lookup(_ks('port'), '5984')))
        # _protocol: Union[str, None] = None
        # try:
        #     _protocol = self._settings.lookup(_ks('protocol'), 'http')
        # except KeyError:
        #     pass
        # if _protocol is None:
        #     _protocol = 'http'
        _username: Union[str, None] = None
        _password: Union[str, None] = None
        try:
            _username = self._settings.lookup(_ks('user'))
            _password = self._settings.lookup(_ks('password'))
        except KeyError:
            pass
        _credentials: PlainCredentials
        if _username is None or \
            _username.strip() == '' or \
            _password is None or \
                _password.strip() == '':
            _credentials = ConnectionParameters.DEFAULT_CREDENTIALS
        else:
            _credentials = PlainCredentials(_username, _password)
        self._client = BlockingConnection(ConnectionParameters(
            host=_host, port=_port, credentials=_credentials))
        self._queue = self._settings.lookup_ns(_ks('queue'))
        self._channel = self._client.channel()

    def _custom_emit(self, record: CustomLogRecord) -> None:
        self._channel.queue_declare(queue=self._queue)
        self._channel.basic_publish(
            exchange='', routing_key=self._queue, body=dumps(_lr2d(record)))

    @staticmethod
    def rabbit_log_listener():
        pass
