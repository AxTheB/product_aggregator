from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', ]


class PriceInfoSerializer(serializers.BaseSerializer):
    """read only serialzer to get price list and trend.
    Requires Product instance, start: datetime and end: datetime

    """

    def __init__(self, instance, start, end, *args, **kwargs):
        """remove start and end from kwargs and call parent constructor"""
        self.start = start
        self.end = end
        super().__init__(instance, *args, **kwargs)

    def to_representation(self, instance):
        offers = instance.offers.all()
        if self.start:
            offers = offers.filter(created__gte=self.start)
        if self.end:
            offers = offers.filter(created__lte=self.end)
        prices = [o.price for o in offers.order_by('created')]
        if len(prices) > 1:
            change = prices[-1] / prices[0] * 100
        else:
            change = 100.0
        return {
            'prices': prices,
            'change': change,
        }
