from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin

from django.contrib import admin
from .models import (UserProfile, Category, Stores, Contacts, Address,
                     MenusStore, Product, Order, CourierGlovo, Review)


class AddressInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Address
    extra = 1

class ContactInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Contacts
    extra = 1

@admin.register(Stores)
class ProductAdmin(TranslationAdmin):
    inlines = [AddressInline, ContactInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Category, MenusStore, Product)
class ProductAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(CourierGlovo)
admin.site.register(Review)


