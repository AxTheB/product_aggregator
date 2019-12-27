from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ProductDetail, ProductList, PriceInfo

app_name = 'product_aggregator'

urlpatterns = [
    path('', ProductList.as_view(), name='product-list'),
    path('<uuid:pk>', ProductDetail.as_view(), name='product-detail'),
    path('<uuid:pk>/prices', PriceInfo.as_view(), name='product-detail-prices'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
