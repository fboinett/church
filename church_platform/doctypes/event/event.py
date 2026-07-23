"""
Event DocType - Church events and gatherings
"""

import frappe
from frappe import _
from church_platform.hierarchy.permissions import get_user_hierarchy_scope, check_hierarchy_access


class Event(frappe.Model):
	"""Church events with hierarchy targeting and registration"""
	
	def validate(self):
		"""Validate event data"""
		# Validate hierarchy targeting
		if self.target_level == 'National':
			self.target_region = None
			self.target_sub_region = None
			self.target_church = None
		elif self.target_level == 'Regional':
			if not self.target_region:
				frappe.throw(_("Target Region is required for Regional events"))
			self.target_sub_region = None
			self.target_church = None
		elif self.target_level == 'Sub-Regional':
			if not self.target_sub_region:
				frappe.throw(_("Target Sub-Region is required for Sub-Regional events"))
			self.target_church = None
		elif self.target_level == 'Local':
			if not self.target_church:
				frappe.throw(_("Target Church is required for Local events"))
		
		# Validate dates
		if self.end_date and self.event_date and self.end_date < self.event_date:
			frappe.throw(_("End date cannot be before event date"))
	
	def on_update(self):
		"""Log event update"""
		frappe.msgprint(
			_("Event '{0}' ({1}) updated successfully").format(self.title, self.status),
			indicator="green",
			alert=True
		)
	
	def get_visible_to_user(self, user=None):
		"""Check if this event is visible to user"""
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
