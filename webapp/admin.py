from django.contrib import admin
from django.core.exceptions import PermissionDenied
from .models import *
from django.contrib.auth.models import User
from import_export.admin import ExportMixin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django_admin_listfilter_dropdown.filters import DropdownFilter
from .resources import *
# Register your models here.


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = ('name', 'category', 'created_at', 'price',)
    list_filter = ('category','school',)
    search_fields = ('name', 'category__name', 'school__name',)
    list_per_page = 10
    readonly_fields = ['created_at']

admin.site.register(Product, ProductAdmin)

class ProductInline(admin.TabularInline):
    model = Product
    fields = ['name', 'created_at', 'school']
    readonly_fields = ['created_at']
    can_delete = False
    show_change_link = True
    extra = 0
    min_num = 0
    max_num = 10
    verbose_name = "Product"
    verbose_name_plural = "Products"
    list_per_page = 10

# Profile Resource (For Export/Import)
class ProfileResource(resources.ModelResource):
    user_username = resources.Field(attribute='user__username', column_name='User Name')
    school_name = resources.Field(attribute='school__name', column_name='School Name')
    class Meta:
        model = Profile
        fields = ('user_username', 'mobile_number', 'school_name',)  # Include the new fields
        export_order = ('user_username', 'mobile_number', 'school_name',)


class UserResource(resources.ModelResource):
    username = resources.Field(attribute='username', column_name='Username')

    class Meta:
        model = User
        fields = ('username',)  # You can add more fields as needed
        export_order = ('username',)  # Add any additional fields in the export order



class ProfileAdmin( ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CombinedUserProfileResource
    list_display = ('user', 'mobile_number', 'school',)
    list_filter = ('school', )

# combine profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = User
    resource_class = UserResource
    inlines = [ProfileInline,]
    field = ["username", "mobile_number", "school"]

class SizeInline(admin.TabularInline):
    model = Size
    extra = 1  # Number of empty forms to display



class CategoriesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [SizeInline, ProductInline]
    list_display = ('name', 'school',)
    search_fields = ('name', 'school',)
    list_filter = ('school', 'name',)

admin.site.register(Categories, CategoriesAdmin)

class SchoolAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    def delete_model(self, request, obj):
        if obj.profile_set.exists():
            raise PermissionDenied("You cannot delete this school because it has associated profiles.")
        super().delete_model(request, obj)
admin.site.register(School, SchoolAdmin)

class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    model = Order
    inlines = [CartItemInline]

class OrderAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderResource
    fields = []
    list_filter = ('school',)
    search_fields = ('name', 'school_name',)
    list_per_page = 20



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Size)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)