from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Post, Category, Tag
from .serializers import (
    PostSerializer, PostDetailSerializer,
    CategorySerializer, CategoryDetailSerializer,
    TagSerializer, TagDetailSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """ POST 增删改查 """
    # 继承自 viewsets.ReadOnlyModelViewSet 代表只读
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    # permission_classes = [IsAdminUser] # 写入时的权限校验

    """ 重写 POST详情 接口 """
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class LatestPostViewSet(PostViewSet):
    """ 最新文章 """
    queryset = Post.latest_posts()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.filter(status=Tag.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TagDetailSerializer
        return super().retrieve(request, *args, **kwargs)

