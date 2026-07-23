"""
Church Blog Post DocType - Blog posts, articles, teachings, testimonies
"""

import frappe
from frappe import _
from church_platform.hierarchy.permissions import get_user_hierarchy_scope, check_hierarchy_access


class ChurchBlogPost(frappe.Model):
	"""Blog posts and publications with moderated comments and social sharing"""
	
	def validate(self):
		"""Validate blog post data"""
		# Validate hierarchy targeting
		if self.target_level == 'National':
			self.target_region = None
			self.target_sub_region = None
			self.target_church = None
		elif self.target_level == 'Regional':
			if not self.target_region:
				frappe.throw(_("Target Region is required for Regional posts"))
			self.target_sub_region = None
			self.target_church = None
		elif self.target_level == 'Sub-Regional':
			if not self.target_sub_region:
				frappe.throw(_("Target Sub-Region is required for Sub-Regional posts"))
			self.target_church = None
		elif self.target_level == 'Local':
			if not self.target_church:
				frappe.throw(_("Target Church is required for Local posts"))
	
	def on_update(self):
		"""Log blog post update"""
		frappe.msgprint(
			_("Blog Post '{0}' ({1}) updated successfully").format(self.title, self.status),
			indicator="green",
			alert=True
		)
	
	def get_visible_to_user(self, user=None):
		"""Check if this blog post is visible to user"""
		if not user:
			user = frappe.session.user
		
		user_scope = get_user_hierarchy_scope()
		if not user_scope:
			return False
		
		return check_hierarchy_access(
			self,
			user_scope,
			self.target_level,
			self.target_region,
			self.target_sub_region,
			self.target_church
		)
	
	def increment_views(self):
		"""Increment view count"""
		self.views_count = (self.views_count or 0) + 1
		frappe.db.set_value(self.doctype, self.name, "views_count", self.views_count)
