from django.http import JsonResponse
import json

from products.models import Product


def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data['title'] = model_data.title
        data['content'] = model_data.content
        data['price'] = model_data.price
    return JsonResponse(data)





#Some bullshit beggining demo
    # request -> HttpRequest -> Django
    # print(request.GET)
    # body = request.body  # byte string of JSON data
    # data = {}
    # try:
    #     data = json.loads(body)  # string of JSON data -> Python dict
    # except:
    #     pass
    # print(data.keys())
    # data['params'] = dict(request.GET)
    # data['headers'] = dict(request.headers)
    # print(request.headers)
    # data['content_type'] = request.content_type
    # print(request.content_type)
    # # return JsonResponse({"message": "This is a Django response"})
    # return JsonResponse(data)
