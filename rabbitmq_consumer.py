# rabbitmq_consumer.py

import pika
import json
from db import update_text_summary
from text_processing import process_text
from config import RABBITMQ_HOST

# RabbitMQ callback function
def callback(ch, method, properties, body):
    try:
        # Parse the message
        data = json.loads(body)
        text_id = data['id']
        text = data['text']
        
        # Process the text (generate summary and tags)
        result = process_text(text)
        summary = result['summary']
        tags = result['tags']
        
        # Update the document in MongoDB
        update_text_summary(text_id, summary, tags)
    except Exception as e:
        print(f"Error processing message: {e}")

# Function to start RabbitMQ consumer
def start_consumer():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()

        # Declare the queue (idempotent operation)
        channel.queue_declare(queue='text_processing_queue')

        # Set up consumer
        channel.basic_consume(queue='text_processing_queue', on_message_callback=callback, auto_ack=True)
        print('Waiting for messages...')
        channel.start_consuming()
    
    except Exception as e:
        print(f"Failed to connect to RabbitMQ: {e}")
