from logging import Handler
from typing import Tuple, Union, Callable, Set, List, Any, AnyStr
from pickle import dumps
from json import loads
from threading import Thread
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from pika.channel import Channel
from pika.spec import Basic, BasicProperties
from tranquillity.settings import ISettings, Yaml
from tranquillity.exceptions import ConnectionException
from .__interfaces import ILogHandler
from .__custom_log_record import CustomLogRecord, _lr2d, _d2lr


def _pika_client(settings: ISettings) -> Tuple[BlockingConnection, str, BlockingChannel]:
    _ks: Callable[[str], Set[str]] = lambda x: {
        x,
        f'rabbitmq.{x}',
        f'conns.rabbitmq.{x}',
        f'rabbit.{x}',
        f'conn.rabbit.{x}',
    }
    _host: Union[str, None] = settings.lookup(_ks('host'))
    if _host is None:
        raise ConnectionException('host is not defined')
    _port: int = int(str(settings.lookup(_ks('port'), '5984')))
    _username: Union[str, None] = None
    _password: Union[str, None] = None
    try:
        _username = settings.lookup(_ks('user'))
        _password = settings.lookup(_ks('password'))
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
    _client: BlockingConnection = BlockingConnection(ConnectionParameters(
        host=_host, port=_port, credentials=_credentials))
    _queue: str = settings.get_ns('log.loggers.rabbitmq.queue')
    _channel: BlockingChannel = _client.channel()
    return _client, _queue, _channel


class RabbitLogHandler(ILogHandler):
    _queue: str
    _client: BlockingConnection
    _channel: BlockingChannel

    def __init__(self, settings: ISettings):
        super().__init__(settings)
        self.initialize_client()

    def initialize_client(self) -> None:
        self._client, self._queue, self._channel = _pika_client(self._settings)

    def _custom_emit(self, record: CustomLogRecord) -> None:
        self._channel.queue_declare(queue=self._queue)
        self._channel.basic_publish(
            exchange='', routing_key=self._queue, body=dumps(_lr2d(record)))

    @staticmethod
    def rabbit_log_listener(handlers: List[Handler], settings: Union[ISettings, None] = None) -> None:
        def _start_consuming(handlers: List[Handler], settings: ISettings) -> None:
            _, _queue, _channel = _pika_client(settings)

            def _consume(ch: Channel, mth: Basic.Deliver, props: BasicProperties, body: Union[str, bytes]):
                if isinstance(body, bytes):
                    body = body.decode('utf-8')
                _log_rec: CustomLogRecord = _d2lr(loads(body))
                for handler in handlers:
                    if isinstance(handler, ILogHandler) and not isinstance(handler, RabbitLogHandler):
                        handler._custom_emit(_log_rec)

            _channel.basic_consume(_queue, _consume, auto_ack=True)
            _channel.start_consuming()
        if settings is None:
            settings = Yaml()
        _thread: Thread = Thread(
            target=_start_consuming, args=(handlers, settings))
        _thread.daemon = True
        _thread.start()
