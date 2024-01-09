from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin

from . import filter
from . import models 
from . import serializers
from . import permission


class CustomerViewSet(ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer


class ProductViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = filter.ProductFilter
    queryset = models.Product.objects.prefetch_related("images").all()
    permission_classes = [permission.IsAdminUserOrReadOnly]
    serializer_class = serializers.ProductSerializer


class CatagoryViewSet(ModelViewSet):
    queryset = models.Catagory.objects.all()
    permission_classes = [permission.IsAdminUserOrReadOnly]
    serializer_class = serializers.CatagorySerializer


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    serializer_class = serializers.CartSerializer
    queryset = models.Cart.objects.all()


class CartItemViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.PostCartItemSerializer
        return serializers.CartItemSerializer
    
    def get_queryset(self):
        return models.CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])
    
    def get_serializer_context(self):
        return { "cart_id": self.kwargs["cart_pk"] }
    


class OrderViewSet(ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


class OrderItemViewSet(ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderItemSerializer


class ReviewViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.ReviewSerializer
    def get_queryset(self):
        return models.Review.objects.select_related("customer").filter(product_id=self.kwargs['product_pk'])
    