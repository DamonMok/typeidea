from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post, Tag, Category
from config.models import SideBar

# Create your views here.

class CommonViewMixin:
	# 通用基础数据：侧边栏、顶部导航栏
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'sidebars':SideBar.get_all(),
		})
		context.update(Category.get_navs())
		return context

# 首页
class IndexView(CommonViewMixin, ListView):
	queryset = Post.latest_posts()
	paginate_by = 2
	context_object_name = 'post_list'
	template_name = 'blog/list.html'

# 分类列表页
class CategoryView(IndexView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		category_id = self.kwargs.get('category_id')
		category = get_object_or_404(Category, pk=category_id)
		context.update({
			'category': category,
		})
		return context

	def get_queryset(self):
		""" 重写queryset, 根据分类过滤"""
		query = super().get_queryset()
		category_id = self.kwargs.get('category_id')
		return queryset.filter(category_id=category_id)

# 标签列表页
class TagView(IndexView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		tag_id = self.kwargs.get('tag_id')
		tag = get_object_or_404(Tag, pk=tag_id)
		context.update({
			'tag': tag,
		})

	def get_queryset(self):
		queryset = super().get_queryset()
		tag_id = self.kwargs.get('tag_id')
		return queryset.filter(tag_id=tag_id)


# 文章详情页
class PostDetailView(CommonViewMixin, DetailView):
	queryset = Post.latest_posts()
	template_name = 'blog/detail.heml'
	context_object_name = 'post'
	pk_url_kwarg = 'post_id'