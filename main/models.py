from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, F
class SiteUser(AbstractUser):
    phone = models.BigIntegerField(blank = True , null = True , unique = True)
    tg_username = models.CharField(max_length=200,blank = True , null = True,unique=True)
    tg_user_id = models.CharField(max_length=10 , unique=True)
    siteusername = models.CharField(max_length = 150)
    SITE_USERS_CHOICE = (
        ('admin', 'Admin'),
        ('client', 'Mijoz'),
        ('manager', 'Menejer'),
        ('driver', 'Haydovchi'),
    )
    userchoice = models.CharField(choices=SITE_USERS_CHOICE )
    joined_date = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.siteusername} ({self.userchoice})"

class MenuCategory(models.Model):
    category_name = models.CharField(max_length = 200)
    slug = models.SlugField(max_length=200, unique=True, null=True)

    class Meta:
        verbose_name_plural = "Menyu kategoriyalari"

    def __str__(self):
        return self.category_name

class Foods(models.Model):
    category = models.ForeignKey(MenuCategory , on_delete=models.CASCADE , related_name='foods')
    name = models.CharField(max_length=200)
    descriptions = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    image = models.ImageField(upload_to='foods/%Y/%m/%d/')
    is_avialable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price}"
class Address(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name="Mijoz ismi")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqami")
    city = models.CharField(max_length=100, default="Toshkent")
    district = models.CharField(max_length=100, verbose_name="Tuman", blank=True, null=True)
    street_address = models.CharField(max_length=255, verbose_name="Ko'cha va uy raqami")
    landmark = models.CharField(max_length=255, blank=True, null=True, verbose_name="Mo'ljal")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.customer_name} - {self.street_address}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Yangi'),
        ('accepted', 'Qabul qilindi'),
        ('cooking', 'Tayyorlanmoqda'),
        ('ready', 'Tayyor'),
        ('on_way', 'Yo\'lda (Kuryerda)'),
        ('delivered', 'Yetkazildi'),
        ('cancelled', 'Bekor qilindi'),
    )

    DELIVERY_TYPE = (
        ('delivery', 'Yetkazib berish'),
        ('pickup', 'Olib ketish (Samo-vyvoz)'),
    )
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='orders')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE, default='delivery')

    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Umumiy summa")
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                         verbose_name="Yetkazib berish narxi")

    comment = models.TextField(blank=True, null=True, verbose_name="Mijoz izohi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Buyurtma #{self.id} ({self.status})"

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"






class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food = models.ForeignKey(Foods, on_delete=models.PROTECT, related_name='order_items')

    quantity = models.PositiveIntegerField(default=1, verbose_name="Soni")
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sotilgan narxi")

    def __str__(self):
        return f"{self.food.name} (x{self.quantity})"

    @property
    def get_total_item_price(self):
        return {self.price_at_order * self.quantity}

    def save(self, *args, **kwargs):
        if not self.price_at_order:
            self.price_at_order = self.food.price
        super().save(*args, **kwargs)


@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    """
    OrderItem qo'shilganda yoki o'chirilganda Order'ning total_price'ini yangilaydi
    """
    order = instance.order
    # Jami summani hisoblash: har bir item (miqdor * narx)
    total = order.items.aggregate(
        total=Sum(F('quantity') * F('price_at_order'))
    )['total'] or 0

    order.total_price = total + order.delivery_price
    order.save()
