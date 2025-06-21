from django.urls import path
from . import views

urlpatterns = [
    path('candidates/', views.candidates_list),
    path('candidates/<int:id>/', views.candidate_detail),
]
