"""
Church Blog Post DocType - Blog posts, articles, teachings, testimonies
"""

import frappe
from frappe.model.document import Document
from frappe import _
from church_platform.hierarchy.permissions import get_user_hierarchy_scope, check_hierarchy_access


class ChurchBlogPost(Document):
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
	
	def get_share_links(self):
		"""Get all social media share links for this blog post"""
		from church_platform.sharing.utils import ContentSharingManager
		
		excerpt = self.excerpt or (self.content[:160] + "...") if self.content else ""
		
		return ContentSharingManager.create_share_links(
			self.doctype,
			self.name,
			self.title,
			excerpt,
			self.featured_image,
			self.author
		)
	
	def get_share_stats(self):
		"""Get sharing statistics for this blog post"""
		from church_platform.analytics.doctype.content_share.content_share import ContentShare
		
		return ContentShare.get_share_stats(self.doctype, self.name)
	
	def log_share(self, platform, device_type="Desktop"):
		"""Log a share event"""
		from church_platform.sharing.utils import ContentSharingManager
		
		# Get current user
		user = frappe.session.user
		member = frappe.db.get_value("Member", {"user": user}, "name")
		
		if member:
			ContentSharingManager.log_share(self.doctype, self.name, member, platform, device_type=device_type)
	
	def get_og_meta_tags(self):
		"""Get Open Graph meta tags for social preview"""
		from church_platform.sharing.utils import OpenGraphMeta
		
		excerpt = self.excerpt or (self.content[:160] + "...") if self.content else ""
		
		og_tags = OpenGraphMeta.generate_tags(
			self.doctype,
			self.name,
			self.title,
			excerpt,
			self.featured_image,
			self.author
		)
		
		return OpenGraphMeta.generate_html_meta_tags(og_tags)
