from django.contrib.admin.models import LogEntry

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea_src.base_admin import BaseOwnerAdmin
from typeidea_src.custom_site import custom_site

import xadmin
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
from xadmin.layout import Row, Fieldset, Container

# Register your models here.

class CategoryOwnerFilter(RelatedFieldListFilter):
	""" 自定义过滤器只展示当前用户分类 """

	@classmethod
	def test(cls, field, request, params, model, admin_view, field_path):
		return field.name == 'category'

	def __init__(self, field, request, params, model, model_admin, field_path):
		super().__init__(field, request, params, model,model_admin, field_path)
		# 重新获取 lookup_choice, 根据 owner 过滤
		self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')

manager.register(CategoryOwnerFilter, take_priority=True)


class PostInline():
	# 在 分类详细页 内置关联数据() 文章编辑
	form_layout = (
		Container(
			Row("title", "desc",)
		)
	)
	extra = 1 # 控制额外多几个
	model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):

	inlines = [PostInline, ] # 在 分类详细页 内置 文章编辑

	list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')

	fields = ('name', 'status', 'is_nav')


	def post_count(self, obj):
		return obj.post_set.count()
	post_count.short_description = '文章数量'



@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
	list_display = ('name', 'status', 'created_time')
	fields = ('name', 'status')



 
@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):

	# 自定义Form(desc摘要字段)
	form = PostAdminForm

	list_display = [
		'title', 'category', 'status',
		'created_time', 'operator', 'owner'
	]

	list_display_links = []

	list_filter = ['category']
	search_fields = ['title', 'category__name']

	actions_on_top = True
	actions_on_bottom = True

 	# 编辑页面
	save_on_top = True

	# 限定要展示的字段、字段的顺序
	# fields = (
	# 	('category', 'title'),
	# 	'desc',
	# 	'status',
	# 	'content',
	# 	'tag',
	# )
	
	# 控制页面的布局
	
	form_layout = (
		Fieldset(
			'基础信息',
			Row("title", "category"),
			'status',
			'tag',
		),
		Fieldset(
			'内容信息',
			'desc',
			'content',
		)
	)

	filter_horizontal = ('tag',) # 多对多控制横竖布局

	def operator(self, obj):
		return format_html(
			'<a href="{}">编辑</a>',
			reverse('xadmin:blog_post_change', args=(obj.id,))
		)
	operator.short_description='操作' # 表头展示名字

	"""
	被抽象到BaseownerAdmin
	def get_queryset(self, request):
		# 根据权限展示文章
		qs = super(PostAdmin, self).get_queryset(request)
		return qs.filter(owner=request.user)

	def save_model(self, request, obj, form, change):
		# owner字段 根据当前用户自动填写
		obj.owner = request.user
		return super(PostAdmin, self).save_model(request, obj, form, change)
	"""

	# (Django自带)添加自定义的JavaScript和CSS
	# class Media:
	# 	css = {
	# 		'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
	# 	}

	# 	js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap/bundle.js', )
	
	# @property
	# def media(self):
	# 	media = super().media
	# 	media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap/bundle.js'])
	# 	media.add_css({
	# 		'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
	# 	})
	# 	return media


# Django的Log配置
# @xadmin.sites.register(LogEntry)
# class LogEntryAdmin(object):
# 	list_display = ['object_repr', 'object_id', 'action_flag', 'user',
# 		'change_message']