from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from usermanagement.models import Student

class ProtectedStudentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not isinstance(user, Student):
            return Response({"error": "Access denied for non-student users."}, status=403)
        
        return Response({"message": f"Welcome, {user.name}!"})
