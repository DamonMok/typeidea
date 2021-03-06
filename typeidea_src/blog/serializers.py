from rest_framework import serializers, pagination

from .models import Post, Category, Tag




class PostSerializer(serializers.HyperlinkedModelSerializer):
    """ 文章列表 """
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        fields = ['url', 'id', 'title', 'category', 'tag', 'owner', 'created_time']
        # 文章列表中分别对应文章详情的url
        extra_kwargs = {
            'url': {'view_name': 'api-post-detail'}
        }


class PostDetailSerializer(PostSerializer):
    """ 文章详情 """
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'owner', 'content_html', 'created_time']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """ 分类列表 """
    class Meta:
        model = Category
        fields = (
            'url', 'id', 'name', 'created_time',
        )
        # 分类列表中分别对应分类详情的url
        extra_kwargs = {
            'url': {'view_name': 'api-category-detail'}
        }


class CategoryDetailSerializer(CategorySerializer):
    posts = serializers.SerializerMethodField('paginated_posts')
    """ 分类详情 """
    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'created_time', 'posts'
        )



class TagSerializer(serializers.HyperlinkedModelSerializer):
    """ 标签列表 """
    class Meta:
        model = Tag
        fields = (
            'url', 'id', 'name', 'created_time',
        )
        # 标签列表中分别对应标签详情的url
        extra_kwargs = {
            'url': {'view_name': 'api-tag-detail'}
        }


class TagDetailSerializer(TagSerializer):
    posts = serializers.SerializerMethodField('paginated_posts')
    """ 标签详情 """
    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'created_time', 'posts'
        )
