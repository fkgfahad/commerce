from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('bids', views.bids, name='bids'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('whitelist', views.whitelist, name='whitelist'),
    path('categories', views.categories, name='categories'),
    path('new_auction', views.new_auction, name='new_auction'),
    path('auctions/<int:auction_id>', views.auction, name='auction'),
    path('categories/<int:category_id>', views.category, name='category'),
    path('auctions/<int:auction_id>/comment', views.comment, name='comment'),
]
