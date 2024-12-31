"""
URL configuration for VideoGame_Vault project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('login/', views.sign_in),
    path('logout/', views.sign_out),
    path('register/', views.sign_up),
    path('populateDB/', views.load_data),
    path('populateRS/', views.load_recommendations_system),
    path('all_video_games/', views.show_all_video_games),
    path('video_game/<int:video_game_id>/', views.show_video_game, name='video_game_detail'),
    path('video_games_selected_developer/', views.show_video_games_selected_developer),
    path('video_games_selected_genre/', views.show_video_games_selected_genre),
    path('video_games_selected_plataform/', views.show_video_games_selected_plataform),
    path('video_games_selected_store/', views.show_video_games_selected_store),
    path('relevant_video_games_with_words/', views.show_relevant_video_games_with_words_in_title_or_description),
    path('relevant_video_games_by_genre_and_words/', views.show_relevant_video_games_selected_genre_and_words_in_title),
    path('relevant_video_games_with_sentence_in_description/', views.show_relevant_video_games_with_sentence_in_description),
    path('video_games_in_period/', views.show_video_games_in_period),
    path('video_games_selected_max_price/', views.show_video_games_selected_max_price),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
