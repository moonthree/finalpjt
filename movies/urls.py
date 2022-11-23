from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('movies/voted/', views.movie_list_voted),
    path('movies/old/', views.movie_list_old),
    path('movies/popular/', views.movie_list_popular),

    path('movies/voted/<int:user_id>/', views.personal_movie_list_voted),
    path('movies/old/<int:user_id>/', views.personal_movie_list_old),
    path('movies/popular/<int:user_id>/', views.personal_movie_list_popular),
    path('movies/clicked/<int:user_id>/', views.movie_list_clicked),
    # 안보고싶은거 조회
    path('movies/unseen/<int:user_id>/', views.movie_list_unseen),
    path('movies/recommend/genre/<int:user_id>/',
         views.movie_list_genre_recommend),
    path('movies/recommend/euclidean/<int:user_id>/',
         views.movie_list_euclidean_recommend),

    path('detail/<int:movie_id>/', views.movie_detail),
    path('detail/video/<int:movie_id>/', views.movie_detail_video),
    path('movies/actors/<int:movie_id>/', views.actor_list),
    path('movies/similar/<int:movie_id>/', views.movie_list_similar),
    # 안보고싶은거 추가하는 url
    path('unseen/<int:movie_id>/', views.movie_unseen),

    path('comments/<int:movie_id>/list/<str:sort>/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_detail),
    path('movies/<int:movie_id>/comments/', views.comment_create),
    path('comments/like/<int:comment_id>/', views.comment_like),

    #     path('comments/like/detail/<int:comment_id>/', views.comment_like_detail),
    #     path('comments/like/list/<int:comment_id>/', views.comment_like_list),
    #     path('comments/like/<int:comment_id>/', views.comment_like_create),




    # # 필수 작성
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # # optional UI
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),

]
