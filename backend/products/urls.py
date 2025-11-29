from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.ProductDetailAPIView.as_view())
]



# # Another way of creating generic views:
# # in views.py need to create the following function:
# # product_detail_view = ProductDetailAPIView.as_view()
# urlpatterns = [
#     path('<int:pk>', views.product_detail_view)
# ]