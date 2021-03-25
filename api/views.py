from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.models import Title, Review
from api.serializers import ReviewSerializer, CommentSerializer
from api.permissions import IsAuthorOrReadOnly

PERMISSION_CLASSES = [IsAuthenticated, IsAuthorOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = PERMISSION_CLASSES

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        params = {
            'author': self.request.user,
            'title_id': self.kwargs.get('title_id')
        }
        get_object_or_404(Title, id=params['title_id'])
        serializer.save(**params)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = PERMISSION_CLASSES

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        comments = review.comments.all()
        return comments
    
    def perform_create(self, serializer):
        params = {
            'author': self.request.user,
            'review_id': self.kwargs.get('review_id')
        }
        get_object_or_404(Review, id=params['review_id'])
        serializer.save(**params)
