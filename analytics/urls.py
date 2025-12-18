from django.urls import path
from .views import recent_top_spenders

urlpatterns = [
    path("customers/recent-top-spenders", recent_top_spenders),
]
