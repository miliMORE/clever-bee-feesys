from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html')


def healthz(request):
    """Public probe. Confirms the app can run SELECT 1."""
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except Exception:
        return JsonResponse({'status': 'unavailable'}, status=503)
    return JsonResponse({'status': 'ok'})
