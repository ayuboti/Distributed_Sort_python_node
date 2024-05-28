import pika
import json

def create_connection():
    # Establish connection to RabbitMQ server
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    return connection

def send_data(queue, data):
    # Send data to a specified queue
    connection = create_connection()
    channel = connection.channel()

    # Ensure the queue exists
    channel.queue_declare(queue=queue)

    # Publish the message
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )
    print(f"Sent data to {queue}: {data}")
    connection.close()

def receive_data(queue, callback):
    # Receive data from a specified queue
    connection = create_connection()
    channel = connection.channel()

    # Ensure the queue exists
    channel.queue_declare(queue=queue)

    # Set up a consumer
    channel.basic_consume(
        queue=queue,
        on_message_callback=callback,
        auto_ack=True
    )

    print(f"Waiting for data in {queue}. To exit press CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()

# Example callback function to process received messages
def process_message(ch, method, properties, body):
    data = json.loads(body)
    print(f"Received {data}")
