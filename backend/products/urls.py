from django.urls import path

from . import views

urlpatterns = [
    # path('', views.ProductListCreateAPIView.as_view()),
    path('', views.ProductMixinView.as_view()),
    # path('<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('<int:pk>/', views.ProductMixinView.as_view()),
    path('<int:pk>/update/', views.ProductUpdateAPIView.as_view()),
    path('<int:pk>/delete/', views.ProductDestroyAPIView.as_view())
]



# # Another way of creating generic views:
# # in views.py need to create the following function:
# # product_detail_view = ProductDetailAPIView.as_view()
# urlpatterns = [
#     path('<int:pk>', views.product_detail_view)
# ]