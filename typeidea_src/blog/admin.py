from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm

# Register your models here.

class CategoryOwnerFilter(admin.SimpleListFilter):
	""" 自定义过滤器只展示当前用户分类 """

	title = '分类过滤器'
	parameter_name = 'owner_category'

	def lookups(self, request, model_admin):
		return Category.objects.filter(owner=request.user).values_list('id', 'name')

	def queryset(self, request, queryset):
		category_id = self.value()
		if category_id:
			return queryset.filter(category_id=self.value())
		return queryset


class PostInline(admin.TabularInline):
	# 在 分类详细页 内置 文章编辑
	fields = ('title', 'desc')
	extra = 1 # 控制额外多1行
	model = Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

	inlines = [PostInline, ] # 在 分类详细页 内置 文章编辑

	list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')

	fields = ('name', 'status', 'is_nav')

	list_filter = [CategoryOwnerFilter]

	def post_count(self, obj):
		return obj.post_set.count()
	post_count.short_description = '文章数量'

	def save_model(self, request, obj, form, change):
		obj.owner = request.user
		return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name', 'status', 'created_time')
	fields = ('name', 'status')

	def save_model(self, request, obj, form, change):
		obj.owner = request.user
		return super(TagAdmin, self).save_model(request, obj, form, change)	

 
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

	# 自定义Form(desc摘要字段)
	form = PostAdminForm

	list_display = [
		'title', 'category', 'status',
		'created_time', 'operator', 'owner'
	]

	list_display_links = []

	list_filter = [CategoryOwnerFilter]
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
	
	fieldsets = (
		('基础配置', {
			'description':'基础配置描述',
			'fields': (
				('title', 'category'),
				'status',
			),
		}),
		('内容', {
			'fields': (
				'desc',
				'content',
			),
		}),
		('额外信息', {
			'classes': ('collapse',), # 隐藏/显示
			'fields': ('tag',),
		})
	)

	filter_horizontal = ('tag',) # 多对多控制横竖布局

	def operator(self, obj):
		return format_html(
			'<a href="{}">编辑</a>',
			reverse('admin:blog_post_change', args=(obj.id,))
		)
	operator.short_description='操作' # 表头展示名字

	def get_queryset(self, request):
		""" 根据权限展示文章 """
		qs = super(PostAdmin, self).get_queryset(request)
		return qs.filter(owner=request.user)

	def save_model(self, request, obj, form, change):
		obj.owner = request.user
		return super(PostAdmin, self).save_model(request, obj, form, change)

	# 添加自定义的JavaScript和CSS
	# class Media:
	# 	css = {
	# 		'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
	# 	}

	# 	js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap/bundle.js', )