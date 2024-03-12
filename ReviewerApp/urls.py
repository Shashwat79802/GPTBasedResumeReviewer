from django.urls import path
from .views import feedback_on_resume

urlpatterns = [
    path('review/', feedback_on_resume, name='feedback_on_resume'),
]