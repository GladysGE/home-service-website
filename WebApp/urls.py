from django.urls import path
from WebApp import views
urlpatterns=[
    path('home_page/', views.home_page, name="home_page"),
    path('about_page/', views.about_page, name="about_page"),
    path('contact_page/', views.contact_page, name="contact_page"),
    path('contact_save/', views.contact_save, name="contact_save"),
    path('portfolio_page/', views.portfolio_page, name="portfolio_page"),
    path('blog_page/', views.blog_page, name="blog_page"),
    path('our_services/', views.our_services, name="our_services"),
    path('filtered_service/<cat_name>/', views.filtered_service, name="filtered_service"),
    path('single_service/<int:sid>/', views.single_service, name="single_service"),
    path('registration_page/', views.registration_page, name="registration_page"),
    path('registration_save/', views.registration_save, name="registration_save"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('cart_page/', views.cart_page, name="cart_page"),
    path('save_cart/', views.save_cart, name="save_cart"),
    path('delete_item/<int:item_id>/', views.delete_item, name="delete_item"),
    path('search_service/', views.search_service, name="search_service"),
    path('booking_page/', views.booking_page, name="booking_page"),
    path('booking_save/', views.booking_save, name="booking_save"),
    path('payment_page/', views.payment_page, name="payment_page"),
    path('demo/', views.demo, name="demo"),

]