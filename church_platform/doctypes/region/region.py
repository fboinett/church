"""
Region DocType (Diocese level)
"""

import frappe
from frappe import _
from church_platform.hierarchy.permissions import get_user_hierarchy_scope


class Region(frappe.Model):
	"""Church hierarchy: Diocese/Region level"""
	
	def validate(self):
		"""Validate region data"""
		# Ensure region code is uppercase
		if self.region_code:
			self.region_code = self.region_code.upper()
	
	def on_update(self):
		"""Log region update"""
		frappe.msgprint(
			_("Region '{0}' updated successfully").format(self.name),
			indicator="green",
			alert=True
		)
