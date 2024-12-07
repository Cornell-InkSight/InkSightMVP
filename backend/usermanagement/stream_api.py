from stream_chat import StreamChat
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os

api_key = os.getenv("STREAM_API_KEY")
api_secret = os.getenv("STREAM_API_SECRET")
chat_client = StreamChat(api_key, api_secret)

@api_view(['GET'])
def get_stream_token(request, user_id):
    """
    Generate a Stream token for the given user_id.
    """
    try:
        if not api_key or not api_secret:
            return Response({"error": "Stream API key or secret is missing"}, status=500)
        token = chat_client.create_token(str(user_id))
        return Response({
            "token": token,
            "user_id": str(user_id)
        }, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def add_stream_permissions(request, user_id):
    chat_client.update_user({
        "id": str(user_id),
        "role": "admin"  
    })
    return Response(f'{user_id} successfully updated')
