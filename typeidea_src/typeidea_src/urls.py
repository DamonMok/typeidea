"""typeidea_src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from blog.views import (
    IndexView, CategoryView, TagView,
    PostDetailView, SearchView, AuthorView,
)
from config.views import LinkListView

from comment.views import CommentView

from typeidea_src.custom_site import custom_site

from django.contrib.sitemaps import views as sitemap_views
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap

import xadmin
xadmin.autodiscover()

from .autocomplete import CategoryAutocomplete, TagAutocomplete

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

# from blog.apis import post_list, PostList

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

from rest_framework import routers
from blog.apis import PostViewSet, CategoryViewSet, LatestPostViewSet, TagViewSet

from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post') # 文章列表、详情
router.register(r'latestpost', LatestPostViewSet, base_name='api-latestpost') # 最新文章列表、详情
router.register(r'category', CategoryViewSet, base_name='api-category') # 分类列表
router.register(r'tag', TagViewSet, base_name='api-tag')

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    re_path(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    re_path(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    re_path(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    re_path(r'links/$', LinkListView.as_view(), name='links'),
    re_path(r'search/$', SearchView.as_view(), name='search'),
    re_path(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    re_path(r'^comment/$', CommentView.as_view(), name='comment'),
    path('super_admin/', admin.site.urls, name='super-admin'),
    path('admin/', xadmin.site.urls, name='xadmin'),

    # Rss/Map
    re_path('rss|feed/$', LatestPostFeed(), name='rss'),
    re_path('sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),

    # 解决外键加载问题
    path('category-autocomplete/', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag-autocomplete'),

    # 图片上传
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # Rest Framework
    # path('api/post/', post_list, name='post-list'),
    # path('api/post/', PostList.as_view(), name='post-list')
    path('api-auth/', include('rest_framework.urls')), # 登录登出
    path('api/', include(router.urls)),

    # 接口文档
    path('api/docs/', include_docs_urls(title='typeidea apis')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
