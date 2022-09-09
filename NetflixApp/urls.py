from django.urls import path
from .views import Home,ProfileList,home,success,ProfileCreate,ShowMovie,ShowMovieDetail,Watch,getlist,moviePurchased,ShowPaidMovieDetail
from . import views
app_name='NetflixApp'

urlpatterns=[
    path('',Home.as_view()),
    path('profile/',ProfileList.as_view(),name='profile_list'),
    path('profile/create/',ProfileCreate.as_view(),name='profile_create'),
    path('watch/<str:profile_id>/',Watch.as_view(),name='watch'),
    path('movie/detail/<str:movie_id>',ShowMovieDetail.as_view(),name='show_det'),
    path('paidmovie/detail/<str:movie_id>',ShowPaidMovieDetail.as_view(),name='show_det_paid'),
    path('movie/play/<str:movie_id>',ShowMovie.as_view(),name='play'),
    path('payment/<int:amt>/<str:title>',views.home,name='payment'),
    path('success',views.success,name='success'),
    path('moviePurchased/<str:movie_title>',views.moviePurchased,name='moviePurchased')
]