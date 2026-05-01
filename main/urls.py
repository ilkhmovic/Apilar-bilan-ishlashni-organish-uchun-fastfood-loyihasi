from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import*

router = DefaultRouter()
router.register(r'users',SiteUserViews,basename='users')
router.register(r'category',MenuCategoryViews,basename='category')
router.register(r'foods',FoodsViews,basename='foods')
router.register(r'address',AddressViews,basename='address')
router.register(r'order',OrderViews,basename='order')
router.register(r'order-item',OrderItemViews,basename='order-item')

urlpatterns = [
    path('api/',include(router.urls))
]