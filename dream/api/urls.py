from django.urls import path
from dream.api.views import DreamListView,DreamDetailView,DreamLikeView,DreamDisLikeView

urlpatterns = [
    path('',DreamListView.as_view(),name='dream-list'),
    path('<int:pk>/like/',DreamLikeView.as_view(),name='dream-like'),
    path('<int:pk>/dislike/',DreamDisLikeView.as_view(),name='dream-dislike'),
    path('<int:pk>/',DreamDetailView.as_view(),name='dream-detail'),
]