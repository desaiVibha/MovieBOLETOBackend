from django.urls import path,re_path
from . import views
from django.views.decorators.csrf import csrf_exempt
from .views import *
urlpatterns=[
    path('signup/', csrf_exempt(SignUpView.as_view()), name='signup'),
    path('signin/', csrf_exempt(SignInView.as_view()),name='signin'),
    path('user-data/', views.user_view),
    path('movielist/',csrf_exempt(GetAllMovies.as_view()),name='movielist'),  
    #re_path(r"^movielist/(?:page(?P<page>[0-9]+))?$",csrf_exempt(GetAllMovies.as_view()),name='movielist'),
    # path('movielist/<slug:?page=<int:page>>',csrf_exempt(GetAllMovies.as_view()),name='movielist'),  
    path('movieDetails/<int:movie_id>',csrf_exempt(GetMovieDetails.as_view()),name='movieDetails'),
    path('getTheatres/<int:movie_id>',csrf_exempt(GetTheatresForMovie.as_view()),name='getTheatresForMovie'),
    # path('gettimings/<int:movie_id>',csrf_exempt(GetTimings.as_view()),name='getTimings'),
    path('addbookedseats/',csrf_exempt(AddBookedSeats.as_view()),name='addBookedSeats'),
    path('addtiming/',csrf_exempt(AddTiming.as_view()),name='addTiming'),
    path('getbookedseats/<str:theatre_name>/<int:movie_id>',csrf_exempt(GetBookedSeats.as_view()),name='getbookedseats'),
    path('moviefilter/',csrf_exempt(MovieFilterApi.as_view()),name='filterMoviesbasedonNameCity'),
]