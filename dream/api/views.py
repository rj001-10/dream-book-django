from rest_framework import generics
from dream.models import Dream
from dream.api.serializers import DreamSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from dream.api.permissions import IsAdminOrReadOnly
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
class DreamListView(generics.ListCreateAPIView):
    serializer_class = DreamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends=[filters.SearchFilter]
    search_fields = ['title','description','user__email','user__first_name','user__last_name']
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Dream.objects.filter(is_active=True)
        
        return Dream.objects.filter(
            is_active=True
        ).filter(Q(user=user) | Q(is_public=True))
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
    

class DreamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dream.objects.all()
    serializer_class = DreamSerializer    
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Dream.objects.filter(is_active=True)
        
        return Dream.objects.filter(
            is_active=True
        ).filter(Q(user=user) | Q(is_public=True))