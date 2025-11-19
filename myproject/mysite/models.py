from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    user_name = models.CharField(max_length=30)
    phone_number = PhoneNumberField()
    RoleChoices = (
        ('owner', 'owner'),
        ('user', 'user'),
        ('courier', 'courier'),
    )
    role = models.CharField(max_length=30, choices=RoleChoices)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Category(models.Model):
    category_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.category_name

class Stores(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_stores')
    store_name = models.CharField(max_length=30, unique=True)
    store_description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    store_image = models.ImageField(upload_to='store_images/')
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store_name} {self.store_description}'

    def get_avg_rating(self):
        rating = self.store_reviews.all()
        if rating.exists():
            return round(sum([i.rating for i in rating]) / rating.count(), 1)
        return 0

    def get_avg_percent(self):
        rating = self.store_reviews.all()
        count_person = 0
        if rating.exists():
            for i in rating:
                if i.rating > 3:
                    count_person += 1
                continue
            return f'{round((count_person * 100) / rating.count(), 1)}%'
        return '0%'

    def get_count_people(self):
        rating = self.store_reviews.all()
        if rating.exists():
            if rating.count() > 3:
                return '3+'
            return rating.count()
        return 0




class Contacts(models.Model):
    store_contact = models.ForeignKey(Stores, on_delete=models.CASCADE, related_name='store_contacts')
    contact_name = models.CharField(max_length=30)
    phone_number = PhoneNumberField()

    def __str__(self):
        return f'{self.contact_name}'

class Address(models.Model):
    store_address = models.ForeignKey(Stores, on_delete=models.CASCADE, related_name='store_addresses')
    address_name = models.CharField(max_length=30)

    def __str__(self):
        return self.address_name

class MenusStore(models.Model):
    stores_menu = models.ForeignKey(Stores, on_delete=models.CASCADE, related_name='stores_menus')
    store_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.store_name

class Product(models.Model):
    product_name = models.CharField(max_length=60)
    description = models.TextField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField(default=1)
    store = models.ForeignKey(MenusStore, on_delete=models.CASCADE, related_name='product_menus')
    product_image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product_name

class Order(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    StatusChoices = (
    ('pending', 'pending'),
    ('canceled', 'canceled'),
    ('delivered', 'delivered'),
    )
    status = models.CharField(max_length=30, choices=StatusChoices)
    delivery_address = models.TextField()
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_orders')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.product}, {self.status}'


class CourierGlovo(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    StatusProductsChoices = (
    ('busy', 'busy'),
    ('available', 'available'),
    )
    status = models.CharField(max_length=30, choices=StatusProductsChoices)
    current_orders = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}, {self.status}'


class Review(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_reviews')
    store = models.ForeignKey(Stores, on_delete=models.CASCADE, null=True, blank=True, related_name='store_reviews')
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='courier_reviews', null=True, blank=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str (i))for i in range(1, 6)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.rating}'








