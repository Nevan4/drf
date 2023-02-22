from django.http import JsonResponse
import json


def api_home(request, *args, **kwargs):
    # request -> HttpRequest -> Django
    body = request.body  # byte string of JSON data
    data = {}
    try:
        data = json.loads(body)  # string of JSON data -> Python dict
    except:
        pass
    print(data.keys())
    # data['headers'] = request.headers
    print(request.headers)
    data['content_type'] = request.content_type
    # return JsonResponse({"message": "This is a Django response"})
    return JsonResponse(data)
