from django.shortcuts import render
from .serializers import*
from .models import*
from rest_framework import viewsets ,filters

class SiteUserViews(viewsets.ModelViewSet):
    queryset = SiteUser.objects.all()
    serializer_class = SiteUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tg_user_id', 'tg_username', 'phone']

class MenuCategoryViews(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = CategorySerializer

class FoodsViews(viewsets.ModelViewSet):
    queryset = Foods.objects.all()
    serializer_class = FoodsSerializer

class OrderViews(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViews(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class AddressViews(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

