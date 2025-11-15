from django.db import models
from decimal import Decimal

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('99.99'))
    
    @property
    def sale_price(self):
        """Computed property: returns formatted sale price (20% discount)."""
        return f"{float(self.price) * 0.8:.2f}"
    
    def get_discount(self):
        """Method: returns discount amount (20% of price).
        Alternative to @property for model-level operations.
        Both approaches can be exposed via SerializerMethodField in DRF.
        """
        return float(self.price) * 0.2