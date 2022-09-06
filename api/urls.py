from django.urls import path
from . import views

urlpatterns = [
    path("cards/", views.CardsGet.as_view()),
    path("card/<uuid:uuid>/", views.CardGet.as_view()),
]
