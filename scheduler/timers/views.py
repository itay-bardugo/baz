from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from scheduler.services.timer import TimerService
import json
from scheduler.exceptions import ApiError


# Create your views here.
@csrf_exempt
def new(request):
    service = TimerService()
    try:
        result = service.new_timer(json.loads(request.body.decode("utf-8")))
    except ApiError as error:
        return JsonResponse(error.to_dict())

    response = {'status': 0, 'data': {'signature': result}}
    return JsonResponse(response)


@require_http_methods(['POST'])
@csrf_exempt
def stop(request, signature):
    service = TimerService()
    try:
        result = service.stop(signature)
    except ApiError as error:
        return JsonResponse(error.to_dict())

    response = {'status': 0, 'data': {'signature': "ok"}}
    return JsonResponse(response)
