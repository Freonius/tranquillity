from logging import Logger
from typing import AnyStr, Union, Any, Callable, Set
from pickle import dumps, loads
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from tranquillity.settings import ISettings
from tranquillity.exceptions import ConnectionException
from .__interface import IConnection


class Rabbit(IConnection):
    _queue: str
    _client: BlockingConnection
    _channel: BlockingChannel
    _settings: ISettings

    def __init__(self, settings: Union[ISettings, None] = None, log: Union[Logger, None] = None) -> None:
        super().__init__(settings, log)
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
        if _username is None or _username.strip() == '' or _password is None or _password.strip() == '':
            _credentials = ConnectionParameters.DEFAULT_CREDENTIALS
        else:
            _credentials = PlainCredentials(_username, _password)
        self._client = BlockingConnection(ConnectionParameters(
            host=_host, port=_port, credentials=_credentials))
        self._queue = self._settings.lookup_ns(_ks('queue'))
        self._channel = self._client.channel()
        if log is not None:
            self.logger(log)

    def send(self, what: Any) -> None:
        self._channel.queue_declare(queue=self._queue)
        self._channel.basic_publish(
            exchange='', routing_key=self._queue, body=dumps(what))

    def listen(self, callback: Callable[[Any, 'Rabbit'], Any]) -> None:
        self._channel.queue_declare(queue=self._queue)

        def _internal_callback(a: Any, b: Any, c: Any, bingpot: AnyStr) -> None:
            if isinstance(bingpot, bytes):
                callback(loads(bingpot), self)
            else:
                callback(bingpot, self)
        self._channel.basic_consume(
            queue=self._queue, on_message_callback=_internal_callback, auto_ack=True)

    def start(self) -> None:
        self._channel.start_consuming()

    def stop(self) -> None:
        self._channel.stop_consuming()

    def delete(self) -> None:
        self._channel.queue_delete(self._queue)

    def connect(self) -> None:
        self.start()

    def close(self) -> None:
        self.stop()
        self.delete()
        self._client.close()

    def _is_connected(self) -> bool:
        return bool(self._client.is_open)

    @property
    def client(self) -> BlockingConnection:
        return self._client

    @property
    def channel(self) -> BlockingChannel:
        return self._channel
