from django.urls import path
from .views import cart_count_api
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    #registration paths starts here:-
    path('school/<slug:slug>/register/', views.register_user, name='register'),
    path('school/<slug:slug>/login/', views.login_user, name='login'),

# Password reset paths
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    path('logout/', views.logout_user, name='logout'),

    path('', views.home, name='home'),

    path('about/',views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('send_message/', views.send_message, name='send_message'),
    path('school/<slug:slug>/products/',views.school_detail, name='school_detail'),
    path('school/<slug:slug>/cart/', views.cart_summary, name='cart_summary'),
    path("school/<slug:slug>/checkout/", views.checkout, name="checkout"),
    path('update-cart/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/count/', cart_count_api, name='cart_count_api'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
