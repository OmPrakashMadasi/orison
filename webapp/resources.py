from import_export import resources
from .models import *

# Resource for User model
class UserResource(resources.ModelResource):
    username = resources.Field(attribute='username', column_name='Username')
    email = resources.Field(attribute='email', column_name='Email')
    is_staff = resources.Field(attribute='is_staff', column_name='Is Staff')

    class Meta:
        model = User
        fields = ('username', 'email', 'mobile_number', 'is_staff')
        export_order = ('username', 'email', 'is_staff')

# Resource for Profile model (replacing both ProfileResource and CombinedUserProfileResource)
class ProfileResource(resources.ModelResource):
    username = resources.Field(attribute='user__username', column_name='Username')
    email = resources.Field(attribute='user__email', column_name='Email')
    mobile_number = resources.Field(attribute='mobile_number', column_name='Mobile Number')
    school_name = resources.Field(attribute='school__name', column_name='School')
    school_address = resources.Field(attribute='school__address', column_name='School Address')

    def dehydrate_school_name(self, profile):
        # Handle case where school is None
        return profile.school.name if profile.school else 'No School'

    def dehydrate_school_address(self, profile):
        return profile.school.address if profile.school else 'No Address'

    class Meta:
        model = Profile
        fields = ('username', 'email', 'mobile_number', 'school_name', 'school_address')
        export_order = ('username', 'email', 'mobile_number', 'school_name', 'school_address')

# Resource for Order model
class OrderResource(resources.ModelResource):
    username = resources.Field(attribute='user__username', column_name='Username')
    email = resources.Field(attribute='user__email', column_name='Email')
    school_name = resources.Field(attribute='school__name', column_name='School Name')
    order_id = resources.Field(attribute='id', column_name='Order ID')
    student_name = resources.Field(attribute='name', column_name='Student Name')
    student_class = resources.Field(attribute='student_class', column_name='Class')
    section = resources.Field(attribute='section', column_name='Section')
    phone = resources.Field(attribute='phone', column_name='Phone')
    address = resources.Field(attribute='address', column_name='Address')
    total_price = resources.Field(attribute='total_price', column_name='Total Price')
    created_at = resources.Field(attribute='created_at', column_name='Created At')
    order_status = resources.Field(attribute='order_status', column_name='Order Status')
    payment_status = resources.Field(attribute='payment_status', column_name='Payment Status')
    items = resources.Field(column_name='Items')

    def dehydrate_items(self, order):
        return "\n".join(
            f"{item.quantity}x {item.product.name} ({item.size.size if item.size else 'No Size'}) - ₹{item.total_price():.2f}"
            for item in order.order_items.all()
        )

    def dehydrate_username(self, order):
        return order.user.username if order.user else 'Guest'

    def dehydrate_email(self, order):
        return order.user.email if order.user else 'N/A'

    class Meta:
        model = Order
        fields = (
            'order_id', 'username', 'email', 'school_name', 'student_name', 'student_class',
            'section', 'phone', 'address', 'items', 'total_price', 'created_at', 'order_status', 'payment_status'
        )
        export_order = (
            'order_id', 'username', 'email', 'school_name', 'student_name', 'student_class',
            'section', 'phone', 'address', 'items', 'total_price', 'created_at', 'order_status', 'payment_status'
        )

# Optionally, add resources for other models if needed (e.g., School, Product)
class SchoolResource(resources.ModelResource):
    class Meta:
        model = School
        fields = ('name', 'address', 'slug', 'is_active', 'created_at')
        export_order = ('name', 'address', 'slug', 'is_active', 'created_at')