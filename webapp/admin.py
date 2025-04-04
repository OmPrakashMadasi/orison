from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django import forms
from .models import *
from import_export.admin import ImportExportModelAdmin, ExportMixin
from .resources import *
from django_select2.forms import Select2Widget
from django.utils.html import format_html
# Inline definitions
class ProductInline(admin.TabularInline):
    model = Product
    fields = ['name', 'created_at', 'school']
    readonly_fields = ['created_at']
    can_delete = False
    show_change_link = True
    extra = 0
    max_num = 10

class SizeInline(admin.TabularInline):
    model = Size
    extra = 1

class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 0

class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0

class OrderItemInlineForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
        widgets = {
            'product': Select2Widget,
            'size': Select2Widget,
        }

    def __init__(self, *args, **kwargs):
        # Extract request from kwargs if available (passed by OrderAdmin)
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Get the user's school from their Profile
        user_school = None
        if request and request.user:
            try:
                profile = request.user.profile  # Assumes Profile has OneToOne with User
                user_school = profile.school
            except (Profile.DoesNotExist, AttributeError):
                user_school = None  # Handle users without a profile/school

        # Filter products and sizes based on user's school
        if user_school:
            self.fields['product'].queryset = Product.objects.filter(school=user_school)
            self.fields['size'].queryset = Size.objects.filter(category__school=user_school)
        else:
            # Fallback: all options if no user school (e.g., superuser)
            self.fields['product'].queryset = Product.objects.all()
            self.fields['size'].queryset = Size.objects.all()

        # If editing an existing OrderItem, respect the Order's school
        if self.instance.pk and self.instance.order and self.instance.order.school:
            order_school = self.instance.order.school
            self.fields['product'].queryset = Product.objects.filter(school=order_school)
            self.fields['size'].queryset = Size.objects.filter(category__school=order_school)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Allow adding new items
    fields = ('product', 'quantity', 'size', 'price')
    form = OrderItemInlineForm


    def get_formset(self, request, obj=None, **kwargs):
        # Pass the request to the form
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.request = request
        return formset


# Admin classes
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'category', 'created_at', 'price')
    list_filter = ('category', 'school')
    search_fields = ('name', 'category__name', 'school__name')
    list_per_page = 10
    readonly_fields = ['created_at']

class SchoolAdmin(ImportExportModelAdmin):
    resource_class = SchoolResource  # Add resource
    list_display = ('name', 'is_active', 'created_at')
    def delete_model(self, request, obj):
        if obj.profile_set.exists():
            raise PermissionDenied("Cannot delete this school; it has associated profiles.")
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.profile_set.exists():
                raise PermissionDenied(f"Cannot delete {obj.name}; it has associated profiles.")
        super().delete_queryset(request, queryset)

class CategoriesAdmin(ImportExportModelAdmin):
    inlines = [ProductInline, SizeInline]
    list_display = ('name', 'school')
    search_fields = ('name',)
    list_filter = ('school', 'name')

class ProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource  # Updated to use consolidated resource
    list_display = ('user', 'mobile_number', 'get_email', 'school')
    list_filter = ('school',)
    search_fields = ('mobile_number',)

    def get_email(self, obj):
        """Return the email from the related User model."""
        return obj.user.email if obj.user else 'N/A'

    get_email.short_description = 'Email'  # Column header in admin

class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    inlines = [ProfileInline]
    list_display = ('username', 'email')

class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = [CartItemInline]
    list_display = ('id', 'user', 'total_price')

class OrderAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderResource
    list_display = ('id', 'name', 'school', 'phone', 'created_at', 'token', 'show_barcode')
    list_filter = ('school','order_status', 'payment_status')
    search_fields = ('phone', 'name', 'school__name')
    readonly_fields = ('created_at', 'barcode_image')
    # readonly_fields = ('created_at', 'show_barcode')
    fields = ('user', 'school', 'name', 'student_class', 'section', 'phone', 'address', 'total_price', 'order_status', 'payment_status', 'barcode_image')
    inlines = [OrderItemInline]
    list_per_page = 20
    ordering = ['-id']
    def show_barcode(self, obj):
        if obj.barcode_image:
            return format_html('<img src="{}" width="100" height="100" alt="QR Code" />', obj.barcode_image.url)
        elif obj.token:
            url = f"/barcode/{obj.token}/"
            return format_html('<img src="{}" width="100" height="100" alt="QR Code" />', url)
        return "No QR code available"

    show_barcode.short_description = "Barcode"

    def get_form(self, request, obj=None, **kwargs):
        # Set default school based on user's Profile when adding a new Order
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Only for new orders
            try:
                profile = request.user.profile
                if profile.school:
                    form.base_fields['school'].initial = profile.school
                    # Optional: make school readonly for non-superusers
                    if not request.user.is_superuser:
                        form.base_fields['school'].disabled = True
            except (Profile.DoesNotExist, AttributeError):
                pass
        return form

    def save_model(self, request, obj, form, change):
        # Set user if not set (optional)
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)
        obj.recalculate_total()



# Register models
admin.site.register(Product, ProductAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Size)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem)
admin.site.register(Message)