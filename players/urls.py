from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.home, name='home'),
    path('players/', views.player_list, name='player_list'),
    path('players/<int:pk>/', views.player_detail, name='player_detail'),
    path('dreamteam/', views.dreamteam_builder, name='dreamteam_builder'),
    path('dreamteams/', views.dreamteam_list_view, name='dreamteam_list_view'),
    path('dreamteams/<int:pk>/delete/', views.dreamteam_delete, name='dreamteam_delete'),
    path('matchups/', views.matchup_analyzer, name='matchup_analyzer'),

    # APIs
    path('api/players/search/', views.player_search_api, name='player_search_api'),
    path('api/dreamteam/save/', views.dreamteam_save, name='dreamteam_save'),
    path('api/matchup/', views.matchup_data_api, name='matchup_data_api'),
]