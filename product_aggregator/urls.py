from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ProductDetail, ProductList, PriceInfo

app_name = 'product_aggregator'

urlpatterns = [
    path('', ProductList.as_view()),
    path('<uuid:pk>', ProductDetail.as_view()),
    path('<uuid:pk>/prices', PriceInfo.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
