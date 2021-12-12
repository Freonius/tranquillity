from logging import Logger
from typing import AnyStr, Union, Any, Callable
from pickle import dumps, loads
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from ..settings import ISettings, Env
from .__interface import IConnection

def _client(settings: Union[ISettings, None] = None) -> BlockingConnection:
    if settings is None:
        settings = Env()
    host: str = str(settings['rabbit.host'])
    port: str = str(settings['rabbit.port'])
    user: str = str(settings['rabbit.user']).strip()
    password: str = str(settings['rabbit.password']).strip()
    if user == ''  or password == '':
        credentials = ConnectionParameters.DEFAULT_CREDENTIALS
    else:
        credentials = PlainCredentials(user, password)
    return BlockingConnection(ConnectionParameters(host=host, port=port, credentials=credentials))


class Rabbit(IConnection):
    _queue: str
    _client: BlockingConnection
    _channel: BlockingChannel
    _settings: ISettings

    def __init__(self, settings: Union[ISettings, None] = None, log: Union[Logger, None] = None) -> None:
        self._client = _client(settings)
        if settings is None:
            settings = Env()
        self._queue = str(settings['rabbit.queue'])
        self._channel = self._client.channel()
        if log is not None:
            self.logger(log)

    def send(self, what: Any) -> None:
        self._channel.queue_declare(queue=self._queue)
        self._channel.basic_publish(exchange='', routing_key=self._queue, body=dumps(what))

    def listen(self, callback: Callable[[Any, 'Rabbit'], Any]) -> None:
        self._channel.queue_declare(queue=self._queue)
        def _internal_callback(a: Any, b: Any, c: Any, bingpot: AnyStr) -> None:
            if isinstance(bingpot, bytes):
                callback(loads(bingpot), self)
            else:
                callback(bingpot, self)
        self._channel.basic_consume(queue=self._queue, on_message_callback=_internal_callback, auto_ack=True)
    
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
        return self._client.is_open

