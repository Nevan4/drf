import json
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse

from products.models import Product

def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data = model_to_dict(model_data, fields=['id', 'title', 'price'])
    return JsonResponse(data)

# JsonResponse automatically handles data type serialization (like Decimal to string)
# while HttpResponse would require manual JSON encoding and type conversion