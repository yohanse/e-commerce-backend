from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from models import *
from serializers import *



class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CatagoryViewSet(ModelViewSet):
    queryset = Catagory.objects.all()
    serializer_class = CatagorySerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderItemSerializer
