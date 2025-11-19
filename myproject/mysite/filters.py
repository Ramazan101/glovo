from .models import Stores, Product
from django_filters import filterset

class StoresFilterSet(filterset.FilterSet):
    class Meta:
        model = Stores
        fields = {
            'category' : ['exact'],

        }



class ProductFilterSet(filterset.FilterSet):
    class Meta:
        model = Product
        fields = {
            'price' : ['gt', 'lt']
        }


