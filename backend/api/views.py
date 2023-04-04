import json
from django.forms.models import model_to_dict
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

# changing old api view into new (django rest framework view):

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        print(instance)
        return Response(serializer.data)

        # print(serializer.data)
        # data = serializer.data
        # return Response(data)


    #
    # instance = Product.objects.all().order_by("?").first()
    # data = {}
    # if instance:
    #     # data = model_to_dict(instance, fields=['id', 'title', 'price', 'sale_price'])
    #     data = ProductSerializer(instance).data
    # # return response with django REST framework display
    # return Response(data)
    # # return only json to display
    # # return JsonResponse(data)

# def api_home(request, *args, **kwargs):
#     model_data = Product.objects.all().order_by("?").first()
#     data = {}
#     if model_data:
#         #by using model_to_dict all data collected from model_data can be parsed to dict
#         data = model_to_dict(model_data)
#         # also only specific params can be picked:
#         # data = model_to_dict(model_data, fields=['id', 'title'])
#         # ---
#         # data['id'] = model_data.id
#         # data['title'] = model_data.title
#         # data['content'] = model_data.content
#         # data['price'] = model_data.price
#     return JsonResponse(data)


# Some bullshit beggining demo
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
