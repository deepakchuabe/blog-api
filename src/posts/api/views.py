from __future__ import unicode_literals

from django.db.models import Q
from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)
#from django_filters.rest_framework import DjangoFilterBackend, SearchFilter

# custom pagination 
from .paginations import PostLimitOffsetPagination, PostPageNumberPagination

from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly
	)
from rest_framework.generics import (
	DestroyAPIView,
	ListAPIView, 
	UpdateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	CreateAPIView,

	)
from .permissions import IsOwnerOrReadOnly
from posts.models import Post 
from .serializers import (
	PostListSerializer ,
	PostDetailSerializer,
	PostCreateUpdateSerializer,)

class PostCreateUpdateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	#update user associtated with post
	permission_classes = [IsAuthenticated]
	def perform_create(self, serializer):
		serializer.save(user = self.request.user)


class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'

class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = 'slug'
	permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
	def perform_create(self, serializer):
		serializer.save(user = self.request.user)

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'


class PostListAPIView(ListAPIView):
	
	serializer_class = PostListSerializer
	filter_backends = [SearchFilter,]
	search_fields = ['title','content','user__first_name']
	# pagination stuf
	pagination_class = PostPageNumberPagination

	def get_queryset(self,*args, **Kwargs):
		queryset_list = Post.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains=query) |
				Q(content__icontains=query) |
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query) 
				).distinct()
		return queryset_list

