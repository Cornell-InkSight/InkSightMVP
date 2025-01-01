from confluent_kafka import Producer

kafka_config = {
    'bootstrap.servers': 'localhost:9092' 
}
producer = Producer(kafka_config)

def send_to_kafka(topic: str, key: str, value: bytes):
    """
    Send a message to a Kafka topic.

    Args:
        topic (str): Kafka topic to send the data.
        key (str): Message key (useful for partitioning).
        value (bytes): Message value (e.g., video chunk).
    """
    try:
        producer.produce(topic, key=key, value=value)
        producer.flush() 
        print(f"Message sent to topic '{topic}'")
    except Exception as e:
        print(f"Failed to send message: {e}")
