from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

#url routing 
urlpatterns = [
    path('',views.index.as_view(), name="index"),                     #class based view
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', views.logout_view),
    path('register/', views.register),
    path('BetOne/<int:id>/',views.BetOneView),
    path('BetFive/<int:id>/',views.BetFiveView),
    path('live_auctions/', views.live_auctions),
    path('auction/',views.auctions),
    path('auction/<int:id>/', views.art_bet),
    path('post/', views.add_post),
    path('posts/', views.get_posts),
    path('listings/',views.listings),
    path('messages/<int:id>/', views.sellermessage),
    path('delete/<int:id>/', views.DeletePost),
    path('messages/', views.messages),
    path('listings/edit/<int:id>/', views.UpdatePost),
    path('like/<int:id>/', views.LikeView),
    path('artchat/<int:id>/', views.art_chat),
    path('comment/<int:post_id>/', views.add_comment),

]
