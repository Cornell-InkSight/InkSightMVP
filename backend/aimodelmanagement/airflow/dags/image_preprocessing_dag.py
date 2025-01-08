from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
from datetime import datetime
import cv2
import base64
import io
import numpy as np
# from image_preprocessing import *
from PIL import Image
import json

def preprocess_image(frame_data, **kwargs):
    """
    Airflow ETL for preprocessing frame-by-frame image from livestream
    Args:
        frame_data (jpeg): serialized image data in JPEG form
    """
    
    result = ""
    return result

def producer_function(data : dict):
    yield json.dumps('data_1'), json.dumps({'data': data})

# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

def run_image_pre_processing(frame_data):
    """
    Defines the worker for image preprocessing
    """
    with DAG(
        'image_preprocessing_dag',
        default_args=default_args,
        description='ETL pipeline for image preprocessing',
        schedule_interval=None,  
    ) as dag:

        preprocess_task = PythonOperator(
            task_id='preprocess_image',
            python_callable=preprocess_image,
            op_kwargs={'frame_data': frame_data},
        )

        preprocess_task
            
        Kafka_Producer = ProduceToTopicOperator(
                                                task_id='Enter_data_to_kafka_topic',
                                                topic=KAFKA_TOPIC,
                                                producer_function=producer_function, 
                                                producer_function_args=["{{ ti.xcom_pull(key='data') }}"],
                                                poll_timeout=10,
                                                dag=dag,
                                                kafka_config={"bootstrap.servers": "localhost:9092"}
        )

