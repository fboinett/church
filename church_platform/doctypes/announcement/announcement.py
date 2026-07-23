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
