# coding:utf-8
from django.contrib import admin

# Register your models here.
from shop.models import Recommend,Product,Sub_category,Category

@admin.register(Recommend)
class RecommendAdmin(admin.ModelAdmin):

    list_display = list_display_links = ('id', 'name', )

    fieldsets = (
        ('Roller', {
            'fields': ('img','name' )
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = list_display_links = ('prod_id', 'prod_name','prod_price','prod_num','prod_brand','prod_sales','prod_cg','show_category','is_delete')
    fieldsets = (
        ('产品基础信息', {
            'fields': ('prod_name','prod_longname','prod_cg','prod_price','prod_num','prod_brand','prod_sales',)
        }),
        ('图片信息', {
            'fields': ('prod_img','prod_rollimg1','prod_rollimg2','prod_rollimg3','prod_rollimg4')
        }),
        ('描述信息', {
            'fields': ('prod_desc',)
        }),
        ('是否已删除', {
            'fields': ( 'is_delete',)
        }),
    )

class Sub_categoryInline(admin.TabularInline):
    model = Sub_category
    extra = 0



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [Sub_categoryInline,]
    list_display = list_display_links = ('id', 'cg_name','rem_order' )

    fieldsets = (
        ('分类(大类信息)', {
            'fields': ('cg_name','rem_order' )
        }),
    )

@admin.register(Sub_category)
class Sub_categoryAdmin(admin.ModelAdmin):

    list_display = list_display_links = ('id', 'cg_name', 'category')

    fieldsets = (
        ('分类(小类信息)', {
            'fields': ('cg_name','category' )
        }),
    )

    fk_fields = ('category',)


