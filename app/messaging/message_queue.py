import json

import pika
from pydantic import json

from schemas import Message
from websocket_connection_manager import WebSocketConnectionManager

# todo: place into config
queue_params = {
    "host": "localhost",
    "port": "5672",
    "heartbeat": "600"
}

# todo: place into config
queue = "queue-name"
exchange = "exchange-name"
routing_key = "routing-key"
exchange_type = "fanout"

websocket_connection_manager = WebSocketConnectionManager()


class MessageQueue:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(**queue_params)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue=queue
        )
        self.channel.exchange_declare(
            exchange=exchange,
            exchange_type=exchange_type
        )
        self.channel.queue_bind(
            exchange=exchange,
            queue=queue,
            routing_key=routing_key
        )

    def publish_message(self, message: Message):
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message.message
        )

    def consume_messages(self):
        try:
            print("Messages are now consumed...")

            async def send_message(ch, method, properties, body):
                print(f" [x] Received {body}")
                message: Message = json.load(body)
                if message:
                    await websocket_connection_manager.broadcast_message_to_group_json(
                        message.group_id,
                        message.message
                    )

            self.channel.basic_consume(
                queue=queue,
                on_message_callback=send_message,
                auto_ack=True
            )
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("Consumer closed.")

    def __del__(self):
        self.connection.close()
