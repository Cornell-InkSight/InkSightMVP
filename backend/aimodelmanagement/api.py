import uuid
from rest_framework.response import Response
import cv2
from subprocess import run, CalledProcessError
import os
from django.http import JsonResponse
from tempfile import NamedTemporaryFile
from django.views.decorators.csrf import csrf_exempt
import shutil
from lecturesessionsmanagement.models import LectureSession
from notepacketsmanagement.models import NotesPacket

KAFKA_TOPIC = "video_data"

@csrf_exempt
def send_video_data_to_ai_model(request, lecture_session_id):
    """
    API Endpoint to send data to the full AI Model pipeline for analysis.
    """
    if request.method == "POST":
        try:
            if 'video_blob' not in request.FILES:
                return JsonResponse({"error": "No video_blob file found in the request."}, status=400)
            
            video_file = request.FILES['video_blob']
            
            with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                for chunk in video_file.chunks():
                    temp_video.write(chunk)
                temp_video_path = temp_video.name
            
            ai_results = run_full_pipeline(lecture_session_id, temp_video_path)

            os.remove(temp_video_path)

            return JsonResponse({"results": ai_results})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method. Only POST allowed."}, status=405)

def run_full_pipeline(lecture_session_id, video_path):
    """
    Run the full pipeline as defined in the documentation.
    Args:
        video_path: Path to the input video file.
    Returns:
        JSON containing processed AI results.
    """
    frames_dir = "aimodelmanagement/lecture_study_guide_fcn/lecture_data/frames"
    videos_dir = "aimodelmanagement/lecture_study_guide_fcn/lecture_data/videos"
    output_dir = "aimodelmanagement/lecture_study_guide_fcn/lecture_data/output"
    pretrain_dir = "aimodelmanagement/models"
    config_path = "aimodelmanagement/lecture_study_guide_fcn/configs/FCN_LectureNet.conf"
        
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(videos_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(pretrain_dir, exist_ok=True)

    try:
        # Step 1: Data Preparation
        extract_frames(video_path, frames_dir)

        # Step 2: Preprocessing
        run(["python", "aimodelmanagement/lecture_study_guide_fcn/binarize.py", config_path, frames_dir, output_dir], check=True)
        run(["python", "aimodelmanagement/lecture_study_guide_fcn/analysis.py", config_path, output_dir], check=True)
        run(["python", "aimodelmanagement/lecture_study_guide_fcn/grouping.py", config_path, output_dir], check=True)
        run(["python", "aimodelmanagement/lecture_study_guide_fcn/segmentation.py", config_path, output_dir], check=True)

        # Step 3: Summary Generation
        run(["python", "aimodelmanagement/lecture_study_guide_fcn/summary.py", config_path, output_dir], check=True)

        ai_results = generate_ai_results(lecture_session_id, output_dir)
        return ai_results

    except CalledProcessError as e:
        raise RuntimeError(f"Pipeline step failed: {e}")
    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)
        shutil.rmtree(output_dir, ignore_errors=True)

def extract_frames(video_path, frames_dir, fps=1):
    """
    Extract frames from the video at specified FPS.
    """
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    interval = int(frame_rate / fps)

    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % interval == 0:
            frame_path = os.path.join(frames_dir, f"frame_{count}.jpg")
            cv2.imwrite(frame_path, frame)
        count += 1

    cap.release()

def generate_ai_results(lecture_session_id, output_dir):
    """
    Generate AI results based on processed pipeline output.
    Args:
        output_dir: Directory containing pipeline outputs.
    Returns:
        JSON summarizing pipeline results.
    """
    lecture_session = LectureSession.objects.get(id=lecture_session_id)
    course = lecture_session.course
    new_packet, created = NotesPacket.objects.get_or_create(notes=output_dir, course=course, lecture_session=lecture_session)
    return {
        "summary": "Pipeline completed successfully.",
        "processed_data": new_packet
    }
