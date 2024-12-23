from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import cv2
import base64
import io
import numpy as np
from .preprocessing_functions import *
from PIL import Image

def preprocess_image(frame_data, **kwargs):
    """
    Airflow ETL for preprocessing frame-by-frame image from livestream
    Args:
        frame_data (jpeg): serialized image data in JPEG form
    """
    # Decode Base64 image
    frame_base64 = frame_data['frame'].split(',')[1]
    decoded_image = base64.b64decode(frame_base64)
    image = Image.open(io.BytesIO(decoded_image))

    # Preprocessing (e.g., resizing and normalization)
    resized_image = load_and_pad_img(image)  
    image_array = np.array(resized_image)
    normalized_image = image_array / 255.0  # Normalize to [0, 1]

    # Encode back to Base64 for storage or transmission
    _, buffer = cv2.imencode('.jpg', normalized_image * 255)
    preprocessed_frame = base64.b64encode(buffer).decode('utf-8')

    # Add metadata for time synchronization
    result = {
        'preprocessed_frame': f"data:image/jpeg;base64,{preprocessed_frame}",
        'metadata': {
            'timestamp': kwargs.get('execution_date').isoformat(),
        },
    }
    print(result)  
    return result

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
