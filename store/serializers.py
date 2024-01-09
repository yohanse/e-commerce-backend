from rest_framework import serializers
from . import models


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.Customer
        fields = ['id', 'user_id','phone', 'birth_date', 'membership']


class ReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = models.Review
        fields = ['id', 'name', 'descritption', 'customer', 'date']


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer()
    class Meta:
        model = models.Product
        fields = ['id', 'title', 'images', 'description', 'unit_price', 'last_update', 'reviews']


class CatagorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = models.Catagory
        fields = ['id', 'title', 'product']


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    product = ProductSerializer()
    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
    
    def get_total_price(self, item: models.OrderItem):
        return item.quantity * item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        models = models.Cart
        fields = ['id', 'items', 'created_at', 'total_price']

    def get_total_price(self, cart: models.Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])


class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model = models.OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']
    
    def get_total_price(self, item: models.OrderItem):
        return item.quantity * item.product.unit_price


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model = models.Order
        fields = ['id', 'items', 'created_at', 'total_price']

    def get_total_price(self, order: models.Order):
        return sum([item.quantity * item.product.unit_price for item in order.items.all()])