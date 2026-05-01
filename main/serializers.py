from rest_framework import serializers
from .models import*

class SiteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteUser
        fields = '__all__'
        read_only_fields = ['tg_username','tg_user_id','joined_date']

        def validate_phone(self, phone):
            clean_phone = phone.replace('+', '').replace(' ', '')
            if not clean_phone.isdigit():
                raise serializers.ValidationError("Telefon raqami faqat raqamlardan iborat bo'lishi kerak.")
            return phone

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        models = MenuCategory
        fields = ['category_name','slug']

class FoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    food_name = serializers.ReadOnlyField(source='food.name')

    class Meta:
        model = OrderItem
        fields = ['food', 'food_name', 'quantity', 'price_at_order']
        extra_kwargs = {'price_at_order': {'read_only': True}}
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'address', 'status', 'delivery_type',
            'total_price', 'delivery_price', 'created_at'
        ]
        # Status va Narxlarni bot o'zgartira olmaydi (Buni backend yoki Signals bajaradi)
        read_only_fields = ['total_price', 'status', 'created_at']

