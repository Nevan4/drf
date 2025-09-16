import json
from django.http import JsonResponse


def api_home(request, *args, **kwargs):
    # reqeuest -> HttpRequest -> Django; no python requests
    # print(dir(request))   # this will return all available methods and attributes of the request object
    body = request.body   # byte strubg of JSON data
    data = {}
    try:
        data = json.loads(body)   # usually takes string of a JSon data and converts it into Python Dictionary
        print(data)
        print(data.keys())
    except:
        pass
    
    try:
        data['headers'] = dict(request.headers)
        data['content_type'] = request.content_type
        data['params'] = dict(request.GET)
    except:
        pass

    print(request.GET)   # url query params

    return JsonResponse(data)
