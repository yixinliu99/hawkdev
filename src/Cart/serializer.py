# apps/carts/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
from items.serializers import ItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'
