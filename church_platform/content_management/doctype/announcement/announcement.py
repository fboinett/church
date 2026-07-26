"""
Announcement DocType - Official communications
"""

import frappe
from frappe import _
from datetime import datetime
from church_platform.hierarchy.permissions import get_user_hierarchy_scope, check_hierarchy_access


class Announcement(frappe.Model):
	"""Official announcements and communications with hierarchy targeting"""
	
	def validate(self):
		"""Validate announcement data"""
		# Validate hierarchy targeting
		if self.target_level == 'National':
			self.target_region = None
			self.target_sub_region = None
			self.target_church = None
		elif self.target_level == 'Regional':
			if not self.target_region:
				frappe.throw(_("Target Region is required for Regional announcements"))
			self.target_sub_region = None
			self.target_church = None
		elif self.target_level == 'Sub-Regional':
			if not self.target_sub_region:
				frappe.throw(_("Target Sub-Region is required for Sub-Regional announcements"))
			self.target_church = None
		elif self.target_level == 'Local':
			if not self.target_church:
				frappe.throw(_("Target Church is required for Local announcements"))
		
		# Set announcement_date to now if not provided
		if not self.announcement_date:
			self.announcement_date = datetime.now()
	
	def on_update(self):
		"""Log announcement update and create readership log entry if published"""
		frappe.msgprint(
			_("Announcement '{0}' ({1}) updated successfully").format(self.title, self.status),
			indicator="green",
			alert=True
		)
	
	def get_visible_to_user(self, user=None):
		"""Check if this announcement is visible to user"""
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
	
	def get_share_links(self):
		"""Get all social media share links for this announcement"""
		from church_platform.sharing.utils import ContentSharingManager
		
		excerpt = self.content[:160] + "..." if len(self.content) > 160 else self.content
		
		return ContentSharingManager.create_share_links(
			self.doctype,
			self.name,
			self.title,
			excerpt,
			self.featured_image,
			self.author
		)
	
	def get_share_stats(self):
		"""Get sharing statistics for this announcement"""
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
