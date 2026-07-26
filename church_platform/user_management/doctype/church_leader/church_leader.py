"""
Church Leader DocType
"""

import frappe
from frappe.model.document import Document
from frappe import _
from datetime import date


class ChurchLeader(Document):
	"""Church leaders at various hierarchy levels"""
	
	def validate(self):
		"""Validate church leader data"""
		# Validate hierarchy assignment
		if self.leadership_level == 'National':
			# National leaders don't need region/sub-region/church
			pass
		elif self.leadership_level == 'Regional':
			if not self.region:
				frappe.throw(_("Region is required for Regional leaders"))
		elif self.leadership_level == 'Sub-Regional':
			if not self.sub_region:
				frappe.throw(_("Sub-Region is required for Sub-Regional leaders"))
		elif self.leadership_level == 'Local':
			if not self.church:
				frappe.throw(_("Church is required for Local leaders"))
		
		# Set email from user if not already set
		if self.user and not self.email:
			user_email = frappe.db.get_value("User", self.user, "email")
			if user_email:
				self.email = user_email
		
		# Set date_joined to today if not provided
		if not self.date_joined:
			self.date_joined = date.today()
	
	def on_update(self):
		"""Log church leader update"""
		frappe.msgprint(
			_("Church Leader '{0}' ({1}) updated successfully").format(self.first_name, self.leadership_level),
			indicator="green",
			alert=True
		)
