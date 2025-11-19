from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (UserProfile, Category, Stores,
                     Order, CourierGlovo, Review, Product)
from .serializers import (UserProfileListSerializer, UserProfileDetailSerializer,
                          CategoryListSerializer,CategoryDetailSerializer,
                          StoresListSerializer, StoresDetailSerializer,
                          ReviewCreateSerializer, ProductSerializer,
                          OrderSerializer, CourierGlovoSerializer,
                          OrderStatusSerializer, StoreCreateSerializer,
                          UserRegisterSerializer, LoginSerializer)
from .permissions import ChekRolePermission, ChekCourierPermission, CreateStorePermission
from .filters import StoresFilterSet, ProductFilterSet
from .pagination import StoresPagination, ProductPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class UserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class StoresListAPIView(generics.ListAPIView):
    queryset = Stores.objects.all()
    serializer_class = StoresListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StoresFilterSet
    ordering_fields = ['created_date']
    search_fields = ['store_name']
    pagination_class = StoresPagination

class StoresDetailAPIView(generics.RetrieveAPIView):
    queryset = Stores.objects.all()
    serializer_class = StoresDetailSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Stores.objects.all()
    serializer_class = StoreCreateSerializer
    permission_classes = [CreateStorePermission]

    def get_queryset(self):
        return Stores.objects.filter(owner=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilterSet
    ordering_fields = ['price']
    search_fields = ['product_name']
    pagination_class = ProductPagination

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [ChekRolePermission]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

class OrderStatusListViewSet(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

class OrderStatusDetailViewSet(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

class CourierGlovoViewSet(viewsets.ModelViewSet):
    queryset = CourierGlovo.objects.all()
    serializer_class = CourierGlovoSerializer
    permission_classes = [ChekCourierPermission]

class ReviewCreteAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [ChekRolePermission]

class ReviewEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [ChekRolePermission]

    def get_queryset(self):
        return Review.objects.filter(client=self.request.user)
