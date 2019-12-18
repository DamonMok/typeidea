from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Post
from .serializers import PostSerializer, PostDetailSerializer


class PostViewSet(viewsets.ModelViewSet):
    """POST 增删改查"""
    # 继承自 viewsets.ReadOnlyModelViewSet 代表只读
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    # permission_classes = [IsAdminUser] # 写入时的权限校验

    """ 重写详情接口 """
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)
