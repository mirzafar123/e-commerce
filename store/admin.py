from django.contrib import admin

from .models import Product , Variation

class ProductAdmin(admin.ModelAdmin):
    list_display= ('name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
# Register your models here.
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'category', 'value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product','category')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)