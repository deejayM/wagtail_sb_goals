# pages/urls.py
from django.urls import path

from .views import DataVisualisationsView, get_data, ChartData

urlpatterns = [
    path('', DataVisualisationsView.as_view(), name='data-visualisations'),
    path('api/data/', get_data, name='api-data'),
    path('api/chart/data/', ChartData.as_view(), name='chart-data'),
]