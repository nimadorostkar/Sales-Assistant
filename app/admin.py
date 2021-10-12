from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Profile, Buyers, Category, Product, Purchase_request
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter, DraggableMPTTAdmin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


admin.site.site_header= " توانکار "
admin.site.site_title= "Tavankar"
admin.site.register(LogEntry)



#------------------------------------------------------------------------------
class ProfileAdmin(ImportExportModelAdmin):
    list_display = ('user_name','phone','address')
    search_fields = ['user_name', 'phone', 'address']

admin.site.register(models.Profile, ProfileAdmin)




#------------------------------------------------------------------------------
class BuyersAdmin(ImportExportModelAdmin):
    list_display = ('name','phone_number','address')
    search_fields = ['name', 'phone_number']

admin.site.register(models.Buyers, BuyersAdmin)



#------------------------------------------------------------------------------
class CategoryMPTTModelAdmin(ImportExportMixin, MPTTModelAdmin, TreeRelatedFieldListFilter):
    mptt_level_indent = 15

admin.site.register(Category, DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title'),
    list_display_links=('indented_title',),)





#------------------------------------------------------------------------------
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'code', 'qty_in_box', 'price_display', 'category', 'image_tag')
    list_filter = ("category", "qty_in_box")
    search_fields = ['name', 'code']
    raw_id_fields = ('category',)

admin.site.register(models.Product, ProductAdmin)






#------------------------------------------------------------------------------
class Purchase_requestAdmin(ModelAdminJalaliMixin,ImportExportModelAdmin):
    list_display = ('product','qty','buyer','method','discount','date','image_tag','status')
    list_filter = ("buyer", "method",'status','date')
    search_fields = ['product', 'buyer']
    raw_id_fields = ('product','buyer')

admin.site.register(models.Purchase_request, Purchase_requestAdmin)












#-------------------------------------------------------- by Nima Dorostkar ---
