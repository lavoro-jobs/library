import time
from typing import Callable

import jsonpickle
import pika
from lavoro_library.model.message_schemas import ItemToMatch


class AMQPConnection:
    def __init__(self, host: str, queue: str):
        self._host = host
        self._queue = queue
        self._connection = None
        self._channel = None
        self._connect()

    def _connect(self):
        try:
            if not self._connection or self._connection.is_closed or not self._connection.is_open:
                params = pika.URLParameters(self._host)
                params.heartbeat = 10
                self._connection = pika.BlockingConnection(params)
                self._channel = self._connection.channel()
                self._channel.queue_declare(queue=self._queue, durable=True)
                print("Connected to RabbitMQ")
        except pika.exceptions.AMQPConnectionError:
            print("Connection was lost. Trying to reconnect...")
            time.sleep(1)
            self._connect()

    def close(self):
        self._connection.close()


class RabbitMQProducer(AMQPConnection):
    def __init__(self, host: str, queue: str):
        super().__init__(host, queue)

    def publish(self, message):
        while True:
            try:
                self._channel.basic_publish(
                    exchange="", routing_key=self._queue, body=jsonpickle.encode(message.model_dump())
                )
                break
            except pika.exceptions.AMQPConnectionError:
                print("Connection was lost. Trying to reconnect...")
                self._connect()
                time.sleep(1)  # Wait before trying to reconnect


class RabbitMQConsumer(AMQPConnection):
    def __init__(self, host: str, queue: str):
        super().__init__(host, queue)

    def consume(self, callback: Callable):
        while True:
            try:
                self._channel.basic_consume(queue=self._queue, on_message_callback=callback, auto_ack=False)
                self._channel.start_consuming()
                break
            except pika.exceptions.AMQPConnectionError:
                print("Connection was lost. Trying to reconnect...")
                self._connect()
                time.sleep(1)

    def _acknowledge(self, method):
        self._channel.basic_ack(delivery_tag=method.delivery_tag)
