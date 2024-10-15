from django.urls import path
from dream.api.views import DreamListView,DreamDetailView

urlpatterns = [
    path('',DreamListView.as_view(),name='dream-list'),
    path('<int:pk>/',DreamDetailView.as_view(),name='dream-detail')
]