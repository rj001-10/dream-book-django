from rest_framework import generics
from dream.models import Dream,DreamLikes
from dream.api.serializers import DreamSerializer,DreamLikeSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q,Count,Exists,OuterRef
from dream.api.permissions import IsAdminOrReadOnly
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class DreamListView(generics.ListCreateAPIView):
    serializer_class = DreamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends=[filters.SearchFilter]
    search_fields = ['title','description','user__email','user__first_name','user__last_name']
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Dream.objects.filter(is_active=True).annotate(
                total_likes=Count('dreamlikes', filter=Q(dreamlikes__is_like=True)),
                total_dislikes=Count('dreamlikes', filter=Q(dreamlikes__is_dislike=True)),
                is_user_liked=Exists(
                    DreamLikes.objects.filter(
                        dream__id=OuterRef('pk'),
                        user=self.request.user,
                        is_like=True
                    )
                ),
                is_user_disliked=Exists(
                    DreamLikes.objects.filter(
                        dream__id=OuterRef('pk'),
                        user=self.request.user,
                        is_like=False
                    )
                ),
            )
        
        return Dream.objects.filter(
            is_active=True
        ).filter(Q(user=user) | Q(is_public=True)).annotate(
                total_likes=Count('dreamlikes', filter=Q(dreamlikes__is_like=True)),
                total_dislikes=Count('dreamlikes', filter=Q(dreamlikes__is_dislike=True)),
                is_user_liked=Exists(
                    DreamLikes.objects.filter(
                        dream__id=OuterRef('pk'),
                        user=self.request.user,
                        is_like=True
                    )
                ),
                is_user_disliked=Exists(
                    DreamLikes.objects.filter(
                        dream__id=OuterRef('pk'),
                        user=self.request.user,
                        is_like=False
                    )
                ),
            )
    
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
            return Dream.objects.filter(is_active=True).annotate(
                total_likes=Count('dreamlikes', filter=Q(dreamlikes__is_like=True)),
                total_dislikes=Count('dreamlikes', filter=Q(dreamlikes__is_dislike=True))
            )
        
        return Dream.objects.filter(
            is_active=True
        ).filter(Q(user=user) | Q(is_public=True)).annotate(
                total_likes=Count('dreamlikes', filter=Q(dreamlikes__is_like=True)),
                total_dislikes=Count('dreamlikes', filter=Q(dreamlikes__is_dislike=True))
            )
        


class DreamLikeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            dream = Dream.objects.get(pk=pk)
            
            dream_like, created = DreamLikes.objects.get_or_create(
                user=request.user,
                dream=dream,
            )

            dream_like.is_like = True
            dream_like.is_dislike = False
            dream_like.save()

            serializer = DreamLikeSerializer(dream_like)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Dream.DoesNotExist:
            return Response({
                'Error': "Dream not found with this ID!"
            }, status=status.HTTP_404_NOT_FOUND)

class DreamDisLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            dream = Dream.objects.get(pk=pk)
            
            dream_like, created = DreamLikes.objects.get_or_create(
                user=request.user,
                dream=dream,
            )

            dream_like.is_like = False
            dream_like.is_dislike = True
            dream_like.save()

            serializer = DreamLikeSerializer(dream_like)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Dream.DoesNotExist:
            return Response({
                'Error': "Dream not found with this ID!"
            }, status=status.HTTP_404_NOT_FOUND)      