from modeltranslation.translator import TranslationOptions,register
from .models import Category, Stores, Contacts, Address, Product, MenusStore

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(Stores)
class StoresTranslationOptions(TranslationOptions):
    fields = ('store_description',)

@register(Contacts)
class ContactsTranslationOptions(TranslationOptions):
    fields = ('contact_name',)

@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('address_name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name',)

@register(MenusStore)
class MenusStoreTranslationOptions(TranslationOptions):
    fields = ('store_name',)