from uuid import uuid4
from rest_framework import serializers
from . import models


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.Customer
        fields = ['id', 'user_id', 'image', 'phone', 'birth_date', 'membership']


class ReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = models.Review
        fields = ['id', 'customer_id', 'name', 'description', 'customer', 'date']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'title', 'images', 'description', 'unit_price', 'last_update']


class CatagorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = models.Catagory
        fields = ['id', 'title', 'product']


class PostCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = models.CartItem
        fields = ['id', 'product_id', 'quantity']

    def validate_product_id(self, value):
        if not models.Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = models.CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except models.CartItem.DoesNotExist:
            self.instance = models.CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance
        


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(method_name='get_total_price', read_only=True)
    product = ProductSerializer()
    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
    
    def get_total_price(self, item: models.OrderItem):
        return item.quantity * item.product.unit_price
    
    def save(self, **kwargs):
        return models.CartItem.objects.create(cart_id=self.context["cart_id"], **self.validated_data)


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(method_name='get_total_price', read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'created_at', 'total_price']

    def get_total_price(self, cart: models.Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])


class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(method_name='get_total_price', read_only=True)
    class Meta:
        model = models.OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']
    
    def get_total_price(self, item: models.OrderItem):
        return item.quantity * item.product.unit_price


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(method_name='get_total_price', read_only=True)
    class Meta:
        model = models.Order
        fields = ['id', 'items', 'created_at', 'total_price']

    def get_total_price(self, order: models.Order):
        return sum([item.quantity * item.product.unit_price for item in order.items.all()])