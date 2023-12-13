from django.urls import path

from .views import *

urlpatterns = [
    path('', PlayersHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addplayer/', AddPlayer.as_view(), name='add_player'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('player/<slug:player_slug>/', ShowPlayer.as_view(), name='player'),
    path('team/<slug:team_slug>/', PlayersTeam.as_view(), name='team'),
    path('delete/<int:player_id>/', delete_player, name='delete_player'),
    path('edit/<int:player_id>/', edit_player, name='edit_player'),
    path('players/', player_list, name='player_list'),
    # path('search/', search_players, name='search_players'),
    path('search/', SearchPlayers.as_view(), name='search_players'),
]
