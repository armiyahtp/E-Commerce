from django.urls import path
from .views import recent_top_spenders, search_orders, generate_report


urlpatterns = [
    path("customers/recent-top-spenders", recent_top_spenders),
    path("orders/search", search_orders),
    path("reports/generate", generate_report),
]
