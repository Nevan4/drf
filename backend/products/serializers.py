from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount'
        ]

    def get_my_discount(self, obj):
        # SerializerMethodField exposes model attributes/methods in the API.
        # Two approaches:
        # 1. @property (e.g., obj.sale_price) — accessed as attribute, read-only
        # 2. method (e.g., obj.get_discount()) — explicit function call
        # Both work here;
        # return obj.get_discount()  # alternative: call the method instead
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()
    