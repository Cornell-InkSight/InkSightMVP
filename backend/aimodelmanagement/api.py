from .airflow.dags.image_preprocessing.image_preprocessing_dag import run_image_pre_processing

def preprocess_image(request, frame_data):
    try:
        run_image_pre_processing(frame_data)
    except:
        print("Image preprocessing failed")