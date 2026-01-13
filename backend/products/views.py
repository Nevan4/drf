from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from typing import cast

from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        print(serializer)
        # serializer.save()
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field - option to set which field we use to look up the object
    # (default is 'pk').
    # Example:
    #   set `lookup_field = 'slug'` in the view and use a URL pattern like
    #   `path('products/<slug:slug>/', ProductDetailAPIView.as_view())`
    #   so the view resolves objects by their `slug` field instead of `pk`.


# # Example of a List Api View. Knowing this we can use also ListCreate API View, which is done above.
# # Remember to add proper routing, example: path('list/', views.ProductListAPIView.as_view())
# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None,  *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)
    
    if method == "POST":
        # create an item
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict, serializer.validated_data)
        
        title = data.get('title')
        content = data.get('content') or title
        serializer.save(content=content)
        return Response(serializer.data, status=201)