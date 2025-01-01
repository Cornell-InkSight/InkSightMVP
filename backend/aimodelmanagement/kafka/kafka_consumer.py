from confluent_kafka import Consumer
import subprocess
import redis

"""Consumer Configuration"""
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'video_processing_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
KAFKA_TOPIC = "video_data"
consumer.subscribe([KAFKA_TOPIC])

"""Redis Configuration"""
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)


def process_video_data(data):
    """
    Processes the video data by running the necessary commands.
    """
    commands = [
        ["python", "pre_ST3D_v3.0_01_binarize.py", "./configs/FCN_LectureNet.conf"],
        ["python", "pre_ST3D_v3.0_02_cc_analaysis.py", "./configs/FCN_LectureNet.conf"],
        ["python", "pre_ST3D_v3.0_02_cc_grouping.py", "./configs/FCN_LectureNet.conf"],
        ["python", "pre_ST3D_v3.0_04_vid_segmentation.py", "./configs/FCN_LectureNet.conf"]
    ]
    for command in commands:
        print(f"Running command: {' '.join(command)}")
        subprocess.run(command) 

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Error Polling for Kafka Topic: {msg.error()}")
        continue

    key = msg.key()
    value = msg.value()
    print(f"Processing message from Kafka Partition {msg.partition()}-->{key()}: {value().decode('utf-8')}")

    processed_video_data = process_video_data(msg.value())

    redis_key = f"video_result:{key}"
    redis_client.set(redis_key, str(processed_video_data))
    print(f"Saved processed video data to Redis cache with key {redis_key}")
    

