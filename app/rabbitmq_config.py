import pika
import json

RABBITMQ_HOST = 'localhost'
EXCHANGE_NAME = 'sorting_exchange'
ROUTING_KEY = 'sort_key'
QUEUE_NAME = 'sorted_queue'

def create_connection():
    # Establish connection to RabbitMQ server
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    return connection

def send_data(data):
    # Send data to the specified queue
    connection = create_connection()
    channel = connection.channel()

    # Ensure the exchange and queue exist
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)

    # Publish the message
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=ROUTING_KEY,
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )
    print(f"Sent data to {QUEUE_NAME}: {data}")
    connection.close()

def receive_data(callback):
    # Receive data from the specified queue
    connection = create_connection()
    channel = connection.channel()

    # Ensure the exchange and queue exist
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)

    # Set up a consumer
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=True
    )

    print(f"Waiting for data in {QUEUE_NAME}. To exit press CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()

# Example callback function to process received messages
def process_message(ch, method, properties, body):
    data = json.loads(body)
    print(f"Received {data}")
