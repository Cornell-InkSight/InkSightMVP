from django.core.management import call_command
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def run_migrations(request):
    try:
        call_command("migrate")
        return JsonResponse({"status": "success", "message": "Migrations applied successfully!"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
