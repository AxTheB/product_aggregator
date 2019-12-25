from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ProductDetail, ProductList

app_name = 'product_aggregator'

urlpatterns = [
    path('', ProductList.as_view()),
    path('<str:pk>', ProductDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
