import datetime

from django.core.exceptions import ValidationError
from django.http import Http404
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .offers import register_product
from .serializers import ProductSerializer, PriceInfoSerializer


class SingleProduct(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
        except ValidationError:  # pk is not valid uuid
            raise Http404


class ProductList(APIView):
    """
    List products, or create a new product.
    Registers product in the Offers microservice and hides unregistered products
    """

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            register_product(product).save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(SingleProduct):
    """
    Retrieve, update or delete a single product.
    """

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        produt = self.get_object(pk)
        serializer = ProductSerializer(produt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PriceInfo(SingleProduct):
    """ Show product prices and change%, optionally between from and to dates"""

    @staticmethod
    def get_date_or_false(to_parse):
        try:
            date = parse_datetime(to_parse)
            if isinstance(date, datetime.datetime):
                return date
        except (TypeError, ValueError):
            pass
        return False

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        print("req.:", request.GET)
        start = self.get_date_or_false(request.GET.get('from', None))
        end = self.get_date_or_false(request.GET.get('to', None))
        print(start, end)
        serializer = PriceInfoSerializer(product, start, end)
        return Response(serializer.data)
