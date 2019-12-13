from django.contrib import admin


class BaseOwnerAdmin:
	"""
	1. 用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
	2. 用来针对 queryset 过滤当前用户的数据(当前用户只能看到当前用户的数据)
	"""

	exclude = ('owner', )

	def get_list_queryset(self):
		request = self.request
		qs = super().get_list_queryset()
		return qs.filter(owner=request.user)

	def save_models(self):
		self.new_obj.owner = self.request.user
		return super().save_models()