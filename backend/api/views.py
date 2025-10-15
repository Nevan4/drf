import json
from django.http import JsonResponse

from products.models import Product

def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data['id'] = model_data.pk
        data['title'] = model_data.title
        data['content'] = model_data.content
        data['price'] = model_data.price
        # next step is to 
        # change the instance of the model (model_data)
        # into a JSON
        # and send it to the client
    return JsonResponse(data)
