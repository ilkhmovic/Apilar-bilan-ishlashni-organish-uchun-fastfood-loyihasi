from django.contrib import admin
from .models import SiteUser , Foods , MenuCategory , Order , OrderItem , Address

@admin.register(SiteUser)
class SiteUserAdmin(admin.ModelAdmin):
    fields = ['siteusername','tg_username','tg_user_id']
    search_fields = ['tg_username','tg_user_id', 'siteusername' , 'phone']
    list_filter = ['joined_date' , 'userchoice']

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    fields = ['category_name','slug']

@admin.register(Foods)
class FoodsAdmin(admin.ModelAdmin):
    fields = ['name','descriptions','price']
    search_fields = ['name']
    list_filter = ['category','price']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone_number', 'city', 'district', 'street_address')
    search_fields = ('customer_name', 'phone_number', 'street_address')
    list_filter = ('city', 'district')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price_at_order',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name_display', 'total_price', 'status', 'delivery_type', 'created_at')
    list_filter = ('status', 'delivery_type', 'created_at')
    search_fields = ('id', 'address__customer_name', 'address__phone_number')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')
    def customer_name_display(self, obj):
        return obj.address.customer_name if obj.address else "Nomsiz"

    customer_name_display.short_description = "Mijoz ismi"
    ordering = ('-created_at',)