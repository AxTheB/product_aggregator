import uuid

from django.db import models


class Token(models.Model):
    """stores app-wide token to offers microservice."""
    value = models.UUIDField()


class TrackedRecord(models.Model):
    """fields common for all microservice objects"""

    class Meta:
        abstract = True
        get_latest_by = "created"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=32, blank=True, null=True)  # TODO: save author from request


class Product(TrackedRecord):
    """Product tracked, corresponds to real-world item"""
    name = models.TextField()
    description = models.TextField()
    registered = models.DateTimeField(blank=True, null=True)


class Offer(TrackedRecord):
    """product is offered for some price somewhere"""
    remote_id = models.IntegerField()  # doc does not
    price = models.IntegerField()
    items_in_stock = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers')
