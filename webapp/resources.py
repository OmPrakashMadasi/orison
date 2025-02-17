# resources.py
from import_export import resources
from .models import *

class CombinedUserProfileResource(resources.ModelResource):
    # Define fields to export
    username = resources.Field(attribute='user__username', column_name='Username')
    email = resources.Field(attribute='user__email', column_name='Email')
    mobile_number = resources.Field(attribute='mobile_number', column_name='Mobile Number')
    school_name = resources.Field(attribute='school__name', column_name='School')
    school_address = resources.Field(attribute='school__address', column_name='School Address')

    # Metaclass to specify the model and the fields
    class Meta:
        model = Profile  # We base the resource on the Profile model
        fields = ('username', 'email', 'mobile_number', 'school_name', 'school_address')  # Order of columns in the export
        export_order = ('username', 'email', 'mobile_number', 'school_name', 'school_address')  # Ensure the right order in the file

class OrderResource(resources.ModelResource):
    username = resources.Field(attribute='user__username', column_name='Username')
    email = resources.Field(attribute='user__email', column_name='Email')
    school_name = resources.Field(attribute='school__name', column_name='School')

    class Meta:
        model = Order
        fields = ('id','username', 'email', 'school_name', 'name', 'student_class', 'section', 'phone', 'address', 'items', 'total_price', 'created_at', )

