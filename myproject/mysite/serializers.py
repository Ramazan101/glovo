from .models import (UserProfile, Category, Stores, Contacts, Address,
                     MenusStore, Product, Order, CourierGlovo, Review)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name']

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class StoresListSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    get_avg_percent = serializers.SerializerMethodField()




    class Meta:
        model = Stores
        fields = ['id', 'store_name','store_image','created_date', 'get_avg_rating', 'get_avg_percent','get_count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_avg_percent(self, obj):
        return obj.get_avg_percent()

    def get_count_people(self, obj):
        return obj.get_count_people()


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_stores = StoresListSerializer(many=True, read_only=True)


    class Meta:
        model = Category
        fields = ['category_name','category_stores']

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['contact_name','phone_number']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_name']


class MenusStoreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenusStore
        fields = ['id','store_name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'product_image']


class MenusStoreDetailSerializer(serializers.ModelSerializer):
    product_menus = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = MenusStore
        fields = ['store_name', 'product_menus']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderStatusSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    client = UserProfileNameSerializer()
    class Meta:
        model = Order
        fields = ['id','client','product','status']


class CourierGlovoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierGlovo
        fields = '__all__'


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    client = UserProfileNameSerializer()
    created_date = serializers.DateTimeField(format('%d/%m/%Y %H:%M'))

    class Meta:
        model = Review
        fields = ['client','comment','rating','created_date','courier']

class StoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stores
        fields = '__all__'

class StoresDetailSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    category = CategoryNameSerializer()
    owner = UserProfileNameSerializer()
    store_contacts = ContactsSerializer(many=True, read_only=True)
    store_addresses = AddressSerializer(many=True, read_only=True)
    stores_menus = MenusStoreDetailSerializer(many=True, read_only=True)
    store_reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Stores
        fields = ['store_name','store_image','created_date','category',
                  'owner','store_contacts','store_addresses',
                  'stores_menus','store_reviews']
